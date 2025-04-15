from src import db

class Transaction(db.Model):
    __tablename__ = 'transactions'
    # Non Nullable Fields
    id = db.Column(db.Integer, primary_key=True, unique=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.Integer, nullable=False)
    
    payee = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payer = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Nullable Fields
    name = db.Column(db.String(40), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=True)
    category = db.Relationship('Category', backref='transactions')
    budget = db.Relationship('Budget', backref='transactions')
    
    # Functional Fields : No control from frontend.
    frozen = db.Column(db.Boolean, nullable=False, default=False)
