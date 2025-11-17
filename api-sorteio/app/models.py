from datetime import datetime
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    raffles_created = db.relationship("Raffle", back_populates="creator")


class Raffle(db.Model):
    __tablename__ = "raffles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), default="OPEN")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime, nullable=True)
    finished_at = db.Column(db.DateTime, nullable=True)

    winner_participant_id = db.Column(
        db.Integer,
        db.ForeignKey("raffle_participants.id"),
        nullable=True
    )

    creator = db.relationship("User", back_populates="raffles_created")

    participants = db.relationship(
        "RaffleParticipant",
        back_populates="raffle",
        foreign_keys="RaffleParticipant.raffle_id"
    )

    winner = db.relationship(
        "RaffleParticipant",
        foreign_keys=[winner_participant_id],
        uselist=False
    )


class RaffleParticipant(db.Model):
    __tablename__ = "raffle_participants"

    id = db.Column(db.Integer, primary_key=True)
    raffle_id = db.Column(db.Integer, db.ForeignKey("raffles.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

    raffle = db.relationship(
        "Raffle",
        back_populates="participants",
        foreign_keys=[raffle_id]
    )

    user = db.relationship("User")
