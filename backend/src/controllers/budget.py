from flask import request, Response, json, Blueprint

budgetBp = Blueprint('budget', __name__)

# POST
def createBudget( budgetDetails : dict ):
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
