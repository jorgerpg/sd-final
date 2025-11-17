from flask import Blueprint, request, jsonify
from app.services import raffle_service
from app.repositories.user_repo import get_user_by_id
from app.utils import decode_jwt
from app.models import RaffleParticipant

bp = Blueprint("raffle", __name__, url_prefix="/api/raffles")


def auth_user(request):
  token = request.headers.get("Authorization")
  if not token:
    return None
  try:
    data = decode_jwt(token.replace("Bearer ", ""))
    return get_user_by_id(data["user_id"])
  except:
    return None


@bp.get("/")
def list_raffles():
  from app.repositories.raffle_repo import get_all
  raffles = get_all()
  return jsonify([
      {
          "id": r.id,
          "title": r.title,
          "status": r.status,
          "creator_id": r.creator_id
      } for r in raffles
  ])


@bp.post("/")
def create_raffle():
  user = auth_user(request)
  if not user:
    return jsonify({"error": "Unauthorized"}), 401

  data = request.json
  r = raffle_service.create_raffle(
      user.id, data["title"], data.get("description"))
  return jsonify({"id": r.id, "message": "Sorteio criado"})


@bp.post("/<int:rid>/join")
def join_raffle(rid):
  user = auth_user(request)
  if not user:
    return jsonify({"error": "Unauthorized"}), 401

  try:
    raffle_service.join_raffle(user.id, rid)
    return jsonify({"message": "Participação registrada"})
  except Exception as e:
    return jsonify({"error": str(e)}), 400


@bp.post("/<int:rid>/start")
def start_raffle(rid):
    user = auth_user(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    try:
        r = raffle_service.start_raffle(user.id, rid)

        winner = None
        if r.winner_participant_id:
            part = RaffleParticipant.query.get(r.winner_participant_id)
            if part:
                winner = {
                    "id": part.user.id,
                    "name": part.user.name,
                    "email": part.user.email
                }

        return jsonify({
            "message": "Sorteio finalizado",
            "winner": winner
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.get("/<int:rid>")
def get_raffle(rid):
    from app.repositories.raffle_repo import get_by_id
    raffle = get_by_id(rid)

    if not raffle:
        return jsonify({"error": "Not found"}), 404

    winner = None
    if raffle.winner_participant_id:
        p = RaffleParticipant.query.get(raffle.winner_participant_id)
        if p:
            winner = {
                "id": p.user.id,
                "name": p.user.name,
                "email": p.user.email
            }

    return jsonify({
        "id": raffle.id,
        "title": raffle.title,
        "description": raffle.description,
        "status": raffle.status,
        "creator_id": raffle.creator_id,
        "winner": winner
    })
