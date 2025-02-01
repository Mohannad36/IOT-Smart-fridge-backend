from flask_sqlalchemy import SQLAlchemy

sqlite = SQLAlchemy()

class User(sqlite.Model):
    id = sqlite.Column(sqlite.Integer, primary_key=True)
    name = sqlite.Column(sqlite.String(80), nullable=False)
    email = sqlite.Column(sqlite.String(120), unique=True, nullable=False)
