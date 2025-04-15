from src import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstname = db.Column(db.String(60))
    lastname = db.Column(db.String(60))
    calling_code = db.Column(db.String(5), nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
