from src import db
from src.constants import CURRENCY_LIST

class Budget(db.Model):
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
            db.Enum(*CURRENCY_LIST, name = 'currency_enum', native_enum=False), 
            nullable=False, 
            default=CURRENCY_LIST[0]
        ) # Suggestion for portability
    duration = db.Column(db.String(40), nullable=True)

    # Relationships
    budgetCycles = db.relationship('BudgetCycle')
    
    activeBudgetCycleId = db.Column(db.Integer, db.ForeignKey('budgetCycles.id'), nullable=True)

    def __init__(self, name, description, creationDate, userId, duration ):
        super().__init__()
        self.name = name
        self.description = description
        self.creationDate = creationDate
        self.userId = userId
        self.duration = duration

    def getDuration(self):
        if self.duration is None:
            return "15"

        return self.duration
