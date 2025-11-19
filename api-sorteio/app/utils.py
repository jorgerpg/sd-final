"""Helpers para geração e validação dos tokens JWT."""

import jwt
from datetime import datetime, timedelta
from flask import current_app


def generate_jwt(user_id: int):
  """Gera um token válido por 24h contendo o ID do usuário."""
  payload = {
      "user_id": user_id,
      "exp": datetime.utcnow() + timedelta(hours=24)
  }
  return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_jwt(token: str):
  """Decodifica e valida o token recebido via header Authorization."""
  return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
