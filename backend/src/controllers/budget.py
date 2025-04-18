from flask import request, Response, json, Blueprint

budgetBp = Blueprint('budget', __name__)

# POST
@budgetBp.route('/create', methods=['POST'])
def createBudget( budgetDetails : dict ):
    # Necessary parameters
    # budgetID, userID, amount, currency
    pass

# DELETE
@budgetBp.route('/delete/<int:id>', methods=['DELETE'])
def deleteBudget(id: int):
    pass

# PUT
@budgetBp.route('/update/<int:id>', methods=['PUT'])
def updateBudget(id: int):
    pass

# PATCH
def updateDescription():
    pass

def updateName():
    pass

# GET
@budgetBp.route('/get/<int:id>', methods=['GET'])
def getBudget(id: int):
    pass

def getBudgetCycles():
    pass

def getBudgetTransactions():
    pass

def getBudgetCategories():
    pass
