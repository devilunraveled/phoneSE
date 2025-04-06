from src import db

class Budget(db.Model):
    __tablename__ = 'budgets'
    
    # Non nullable Fields
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    creationDate = db.Column(db.DateTime, nullable=False)
    
    accounts = db.Relationship('Account', backref='budget')
    categories = db.Relationship('Category', backref='budget')

    # Nullable Fields
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    budgetCycles = db.Relationship('BudgetCycle', backref='budget')
