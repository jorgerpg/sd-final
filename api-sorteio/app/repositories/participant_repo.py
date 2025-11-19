"""Operações de CRUD relacionadas à tabela de participantes."""

from app.models import RaffleParticipant
from app.extensions import db


def add_participant(part: RaffleParticipant):
  """Registra a entrada de um usuário em um sorteio."""
  db.session.add(part)
  db.session.commit()
  return part


def find_participation(raffle_id, user_id):
  """Verifica se o usuário já está inscrito no sorteio."""
  return RaffleParticipant.query.filter_by(
      raffle_id=raffle_id,
      user_id=user_id
  ).first()


def get_participants(raffle_id):
  """Retorna todas as participações de um sorteio."""
  return RaffleParticipant.query.filter_by(raffle_id=raffle_id).all()
