from src import db

class Account(db.Model):
    """
        Backend for any source / wallet / account that can 
        be used to make transactions.
    """

    __tablename__ = 'accounts'

    # Non Nullable Fields
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    currency = db.Column(db.Integer, nullable=False)
    
    # Nullable Fields
    budget = db.Relationship('Budget', backref='account')
    description = db.Column(db.String(100), nullable=True)
