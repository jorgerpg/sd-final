import random
from datetime import datetime
from app.models import Raffle, RaffleParticipant
from app.repositories import raffle_repo, participant_repo
from app.extensions import db


def create_raffle(creator_id, title, description):
  raffle = Raffle(
      title=title,
      description=description,
      creator_id=creator_id
  )
  return raffle_repo.create_raffle(raffle)


def join_raffle(user_id, raffle_id):
  raffle = raffle_repo.get_by_id(raffle_id)

  if raffle.status != "OPEN":
    raise ValueError("Sorteio não está aberto.")

  if participant_repo.find_participation(raffle_id, user_id):
    raise ValueError("Você já entrou neste sorteio.")

  participant = RaffleParticipant(
      raffle_id=raffle_id,
      user_id=user_id
  )

  return participant_repo.add_participant(participant)


def start_raffle(creator_id, raffle_id):
  raffle = raffle_repo.get_by_id(raffle_id)

  if raffle.creator_id != creator_id:
    raise PermissionError("Apenas o criador pode iniciar.")

  if raffle.status != "OPEN":
    raise ValueError("Sorteio já foi iniciado ou finalizado.")

  participants = participant_repo.get_participants(raffle_id)
  if not participants:
    raise ValueError("Sem participantes.")

  winner = random.choice(participants)

  raffle.status = "FINISHED"
  raffle.started_at = datetime.utcnow()
  raffle.finished_at = datetime.utcnow()
  raffle.winner_participant_id = winner.id

  db.session.commit()
  return raffle
