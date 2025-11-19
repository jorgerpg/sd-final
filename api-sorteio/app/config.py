"""Configurações centrais do aplicativo Flask."""

import os


class Config:
  """Encapsula valores carregados do ambiente para o Flask/SQLAlchemy."""

  # Chave usada para assinar JWTs e sessões server-side.
  SECRET_KEY = os.getenv("SECRET_KEY", "change_me")

  # URL do banco. Por padrão mira o Postgres do docker-compose.
  SQLALCHEMY_DATABASE_URI = os.getenv(
      "DATABASE_URL",
      "postgresql://sorteio_user:senha123@db:5432/sorteio_db"
  )

  # Evita o overhead do recurso de track modifications do SQLAlchemy.
  SQLALCHEMY_TRACK_MODIFICATIONS = False


def get_config():
  """Retorna a classe de configuração para facilitar testes/trocas."""
  return Config
