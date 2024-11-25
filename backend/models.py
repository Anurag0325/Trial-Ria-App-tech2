from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Colleagues(db.Model):
    __tablename__ = 'colleagues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)


class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    options = db.Column(db.JSON, nullable=False)
    answer = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "question_text": self.question_text,
            "options": self.options,
            "answer": self.answer
        }


class Reports(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    colleague_id = db.Column(db.Integer, db.ForeignKey(
        'colleagues.id'), nullable=False)
    clicked = db.Column(db.Boolean, default=False)
    answered = db.Column(db.Boolean, default=False)
    answers = db.Column(db.PickleType)
    score = db.Column(db.Float)
    status = db.Column(db.String(50), default="Pending")
    clicked_date = db.Column(db.DateTime)
    colleague = db.relationship(
        'Colleagues', backref=db.backref('reports', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "colleague": {
                "name": self.colleague.name,
                "email": self.colleague.email
            },
            "score": self.score,
            "status": self.status,
            "answers": self.answers,
            "answered": self.answered,
            "clicked": self.clicked,
            "clicked_date": self.clicked_date.strftime('%Y-%m-%d') if self.clicked_date else None
        }


class EmailLogs(db.Model):
    __tablename__ = 'email_logs'
    id = db.Column(db.Integer, primary_key=True)
    colleague_id = db.Column(db.Integer, db.ForeignKey(
        'colleagues.id'), nullable=False)
    email_address = db.Column(db.String(120), nullable=False)
    # Timestamp of when the email was sent
    sent_date = db.Column(db.DateTime, default=datetime.utcnow)

    colleague = db.relationship(
        'Colleagues', backref=db.backref('email_logs', lazy=True))
