"""Regras de negócio relacionadas à autenticação."""

from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.repositories import user_repo
from app.utils import generate_jwt


def register_user(name, email, password):
  """
  Garante unicidade de e-mail, salva o usuário e devolve o registro.

  Levanta `ValueError` quando o e-mail já está em uso.
  """
  if user_repo.find_by_email(email):
    raise ValueError("Email já cadastrado.")

  hashed = generate_password_hash(password)
  user = User(name=name, email=email, password_hash=hashed)
  return user_repo.create_user(user)


def login(email, password):
  """
  Valida credenciais e devolve um par (token JWT, usuário).

  `ValueError` é lançado quando e-mail ou senha são inválidos.
  """
  user = user_repo.find_by_email(email)
  if not user or not check_password_hash(user.password_hash, password):
    raise ValueError("Login inválido.")

  token = generate_jwt(user.id)
  return token, user
