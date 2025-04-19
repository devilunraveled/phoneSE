from sqlalchemy.orm import Mapped
from dataclasses import dataclass
from datetime import datetime
from typing import List

from src import db
from src.constants import CURRENCY_LIST
from .budgetCycle import BudgetCycle

@dataclass
class Budget(db.Model):
    id: int
    name: str
    description: str
    creationDate: datetime
    userId : int
    amount: float
    currency: str
    duration: int
    budgetCycles: Mapped[List[BudgetCycle]]
    activeBudgetCycleId: int

    __tablename__ = 'budgets'
    
    # Non nullable Fields
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    creationDate = db.Column(db.DateTime, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Nullable Fields
    amount = db.Column(db.Float, nullable=True, default=0.0)
    currency = db.Column(
            db.String(4), 
            nullable=False, 
            default=CURRENCY_LIST[0]
        ) # Suggestion for portability
    duration = db.Column(db.Integer, nullable=True)

    # Relationships
    budgetCycles = db.relationship('BudgetCycle', foreign_keys='BudgetCycle.budgetId')
    
    activeBudgetCycleId = db.Column(db.Integer, db.ForeignKey('budgetCycles.id'), nullable=True)

    def getDuration(self):
        if self.duration is None:
            return 15

        return self.duration
