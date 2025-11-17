from app.models import User
from app.extensions import db


def find_by_email(email: str):
  return User.query.filter_by(email=email).first()


def create_user(user: User):
  db.session.add(user)
  db.session.commit()
  return user


def get_user_by_id(uid: int):
  return User.query.get(uid)
