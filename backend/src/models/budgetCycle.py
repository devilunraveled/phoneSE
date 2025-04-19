from sqlalchemy import Table, Column
from sqlalchemy.orm import Mapped
from dataclasses import dataclass
from datetime import datetime
from typing import List

from src import db
from src.constants import CURRENCY_LIST
from .transaction import Transaction

transactionBudgetCycleAssociation = Table(
    'transactionBudgetCycleAssociation',
    db.Model.metadata,
    Column('budgetCycleId', db.Integer, db.ForeignKey('budgetCycles.id')),
    Column('transactionId', db.Integer, db.ForeignKey('transactions.id')),
    keep_existing=True
)

@dataclass
class BudgetCycle(db.Model):
    id: int
    amount: float
    currency: int
    startDate: datetime
    duration: int
    budgetId: int
    transactions: Mapped[List[Transaction]]

    __tablename__ = 'budgetCycles'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(
            db.String(4), 
            nullable=False, 
            default=CURRENCY_LIST[0]
        )

    startDate = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    budgetId = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)
    transactions = db.relationship('Transaction', secondary=transactionBudgetCycleAssociation)
