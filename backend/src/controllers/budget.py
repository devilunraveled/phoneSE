from typing import Optional
from src.models.budget import Budget

# POST
def createBudget( ) ->Optional[Budget]:
    # Necessary parameters
    # budgetID, userID, amount, currency
    pass

# DELETE
def deleteBudget(id: int):
    pass

# PUT
def updateBudget(id: int):
    pass

# PATCH
def updateDescription():
    pass

def updateName():
    pass

# GET
def getBudget(id: int):
    pass

def getBudgetCycles():
    pass

def getBudgetTransactions():
    pass

def getBudgetCategories():
    pass
