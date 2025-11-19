"""Blueprint de autenticação com endpoints de registro e login."""

from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login
from app.utils import decode_jwt

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/register")
def register():
  """Cria um novo usuário e devolve o ID gerado."""
  data = request.json
  try:
    u = register_user(data["name"], data["email"], data["password"])
    return jsonify({"message": "Usuário criado", "id": u.id})
  except Exception as e:
    return jsonify({"error": str(e)}), 400


@bp.post("/login")
def login_user():
  """Valida credenciais e retorna o token + dados básicos."""
  data = request.json
  try:
    token, user = login(data["email"], data["password"])
    return jsonify({
        "token": token,
        "user": {"id": user.id, "name": user.name, "email": user.email}
    })
  except Exception as e:
    return jsonify({"error": str(e)}), 400
