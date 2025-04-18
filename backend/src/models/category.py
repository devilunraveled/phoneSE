from dataclasses import dataclass

from src import db

@dataclass
class Category(db.Model):
    id: int
    name: str
    description: str
    budgetId: int
    
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40), nullable=False)

    description = db.Column(db.String(100), nullable=True)
    
    budgetId = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=True)
    # Category budget should by default have all account as available source accounts.
    # If the user creates a new source account, this should be reflected as well.
