from src import db
from dataclasses import dataclass
from src.constants import CURRENCY_LIST

@dataclass
class Account(db.Model):
    """
        Backend for any source / wallet / account that can 
        be used to make transactions.
    """
    id : int
    name : str
    userId : int
    balance : float
    currency : str
    budget : int
    description : str

    __tablename__ = 'accounts'

    # Non Nullable Fields
    id = db.Column(db.Integer, primary_key=True, unique=True)
    
    name = db.Column(db.String(40), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    currency = db.Column(
            db.Enum(*CURRENCY_LIST, name = 'currency_enum', native_enum=False), 
            nullable=False, 
            default=CURRENCY_LIST[0]
        ) # Suggestion for portability
    
    # Nullable Fields
    budgetId = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=True)
    description = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '<%r Account>' % self.name
