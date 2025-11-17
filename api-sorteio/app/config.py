import os


class Config:
  SECRET_KEY = os.getenv("SECRET_KEY", "change_me")

  SQLALCHEMY_DATABASE_URI = os.getenv(
      "DATABASE_URL",
      "postgresql://sorteio_user:senha123@db:5432/sorteio_db"
  )

  SQLALCHEMY_TRACK_MODIFICATIONS = False


def get_config():
  return Config
