from src import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstName = db.Column(db.String(60))
    lastName = db.Column(db.String(60))
    countryCode = db.Column(db.String(5), nullable=False)
    phoneNumber = db.Column(db.String(12), unique=True, nullable=False)
    passwordHash = db.Column(db.String(128), nullable=False)
    budgetId = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=True)
