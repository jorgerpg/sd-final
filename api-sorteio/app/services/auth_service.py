from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.repositories import user_repo
from app.utils import generate_jwt


def register_user(name, email, password):
  if user_repo.find_by_email(email):
    raise ValueError("Email já cadastrado.")

  hashed = generate_password_hash(password)
  user = User(name=name, email=email, password_hash=hashed)
  return user_repo.create_user(user)


def login(email, password):
  user = user_repo.find_by_email(email)
  if not user or not check_password_hash(user.password_hash, password):
    raise ValueError("Login inválido.")

  token = generate_jwt(user.id)
  return token, user
