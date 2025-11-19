"""Acesso aos dados dos sorteios."""

from app.models import Raffle
from app.extensions import db


def create_raffle(raffle: Raffle):
  """Insere um novo sorteio na base e retorna o objeto persistido."""
  db.session.add(raffle)
  db.session.commit()
  return raffle


def get_all():
  """Recupera todos os sorteios (sem filtro/paginação)."""
  return Raffle.query.all()


def get_by_id(rid: int):
  """Busca um sorteio específico pelo ID."""
  return Raffle.query.get(rid)


def save():
  """Commit genérico para quando apenas atributos são alterados."""
  db.session.commit()
