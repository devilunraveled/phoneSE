from sqlalchemy import Table, Column

from src import db

# transactionCategoryAssociation = Table(
#     'transactionCategoryAssociation',
#     db.Model.metadata,
#     Column('transactionId', db.Integer, db.ForeignKey('transactions.id')),
#     Column('categoryId', db.Integer, db.ForeignKey('categories.id')),
#     keep_existing=True
# )

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

    # Relationships
    # categories = db.relationship('Categories', secondary=transactionCategoryAssociation)
    
    # Functional Fields : No control from frontend.
    frozen = db.Column(db.Boolean, nullable=False, default=False)
