from app.models import RaffleParticipant
from app.extensions import db


def add_participant(part: RaffleParticipant):
  db.session.add(part)
  db.session.commit()
  return part


def find_participation(raffle_id, user_id):
  return RaffleParticipant.query.filter_by(
      raffle_id=raffle_id,
      user_id=user_id
  ).first()


def get_participants(raffle_id):
  return RaffleParticipant.query.filter_by(raffle_id=raffle_id).all()
