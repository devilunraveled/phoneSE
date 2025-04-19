from sqlalchemy import Table, Column
from sqlalchemy.orm import Mapped
from dataclasses import dataclass
from datetime import datetime
from typing import List

from src import db
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
    name: str
    description: str
    amount: float
    currency: int
    startDate: datetime
    endDate: datetime
    budgetId: int
    transactions: Mapped[List[Transaction]]

    __tablename__ = 'budgetCycles'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.Integer, nullable=False)

    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)

    budgetId = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)
    parentBudget = db.relationship('Budget', back_populates='budgetCycles')

    transactions = db.relationship('BudgetCycle', secondary=transactionBudgetCycleAssociation)