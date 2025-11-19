"""Repositório com operações básicas de persistência para `User`."""

from app.models import User
from app.extensions import db


def find_by_email(email: str):
  """Retorna o usuário com o e-mail informado ou `None`."""
  return User.query.filter_by(email=email).first()


def create_user(user: User):
  """Persiste o usuário e devolve a instância já sincronizada."""
  db.session.add(user)
  db.session.commit()
  return user


def get_user_by_id(uid: int):
  """Busca um usuário pelo ID primário."""
  return User.query.get(uid)
