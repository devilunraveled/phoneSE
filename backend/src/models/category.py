from src import db

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40), nullable=False)
    transactions = db.relationship('Transaction', backref='category')
    
    description = db.Column(db.String(100), nullable=True)
    transactions = db.relationship('Transaction', backref='category')
    
    budgets = db.relationship('Budget', backref='category')
    # Category budget should by default have all account as available source accounts.
    # If the user creates a new source account, this should be reflected as well.
