from app.models import Raffle
from app.extensions import db


def create_raffle(raffle: Raffle):
  db.session.add(raffle)
  db.session.commit()
  return raffle


def get_all():
  return Raffle.query.all()


def get_by_id(rid: int):
  return Raffle.query.get(rid)


def save():
  db.session.commit()
