from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))
    created = db.Column(db.DateTime)

    def __repr__(self):
        return f"User {self.email}"

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email
        }
