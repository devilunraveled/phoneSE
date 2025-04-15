from src import db

class BudgetCycle(db.Model):
    __tablename__ = 'budgetCycles'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.Integer, nullable=False)

    startDate = db.Column(db.DateTime, nullable=False)
    endDate = db.Column(db.DateTime, nullable=False)

    budgetId = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)

    transactions = db.relationship('Transaction', backref='budgetCycle')
