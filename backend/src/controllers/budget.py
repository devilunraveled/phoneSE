from datetime import datetime, timedelta
from typing import Optional

from src import PhoneSELogger
from src.utils import checkIfExpired, getStartDateOfCurrentCycle

from src.models.budget import Budget
from src.models.budgetCycle import BudgetCycle
from src.models.category import Category
from src.models.transaction import Transaction
from src.models.account import Account
from src.models.user import User

from src.controllers.user import checkIfUserExists
from src.controllers.budgetCycle import createBudgetCycle, getBudgetCycleTransactions, getBudgetCycle

# POST
def createBudget( name, userId, duration = None, description = None ) ->Optional[tuple[Budget, BudgetCycle]]:
    if not checkIfUserExists( userId ):
        PhoneSELogger.error( "Budget creation failed: User does not exist" )
        return None

    try:
        if description is None:
            description = ""

        PhoneSELogger.info(f"Creating budget: {name}")
        createTime = datetime.now()
        budget = Budget(
                name=name, 
                userId=userId, 
                duration=duration, 
                description=description,
                creationDate=createTime)
        
        newBudgetCycle = createBudgetCycle(budget, createTime)
        if newBudgetCycle is None:
            PhoneSELogger.error("Budget creation failed: Failed to create budget cycle")
            return None

        budget.budgetCycles.append(newBudgetCycle)
        budget.activeBudgetCycleId = newBudgetCycle.id

        PhoneSELogger.info(f"Budget created: {budget}")
        return budget, newBudgetCycle
    except Exception as e:
        PhoneSELogger.error(f"Failed to create budget: {e}")
        return None

# PUT
def updateBudget(id: int, **kwargs):
    try :
        PhoneSELogger.info(f"Updating budget: {id}")
        budget = getBudget(id)
        
        if budget is None:
            PhoneSELogger.error("Budget update failed: Budget does not exist")
            return None

        for key, value in kwargs.items(): #?? Unsafe as it is.
            if not hasattr( budget, key ):
                PhoneSELogger.error(f"Budget update failed: Invalid attribute : {key}")
                return None
            setattr( budget, key, value )
            PhoneSELogger.debug(f"Budget updated: {key} : {value}")

        PhoneSELogger.info( "Budget updated successfully" )
        return budget
    except Exception as e:
        PhoneSELogger.error(f"Failed to update budget: {e}")
        return None

# GET
def getBudget(id: int):
    try :
        PhoneSELogger.info(f"Getting budget: {id}")
        budget = Budget.query.get(id)
        return budget
    except Exception as e:
        PhoneSELogger.error(f"Failed to get budget: {e}")
        return None

def createNewBudgetCycle( budgetId ):
    try :
        budget = getBudget(budgetId)
        if budget is None:
            PhoneSELogger.error("Failed to create new budget cycle: Budget does not exist")
            return None
        
        # Make the new cycle active.
        newBudgetCycle : BudgetCycle = createBudgetCycle(budget)

        budget.budgetCycles.append(newBudgetCycle)
        budget.activeBudgetCycleId = newBudgetCycle.id

        return newBudgetCycle, budget 

    except Exception as e:
        PhoneSELogger.error(f"Failed to create new budget cycle: {e}")
        return None
        

def getBudgetCycles( budgetId ) -> Optional[list[BudgetCycle]]:
    try :
        budget = getBudget(budgetId)
        if budget is None:
            PhoneSELogger.error("Failed to get budget cycles: Budget does not exist")
            return None

        budgetCycles = budget.budgetCycles
        return budgetCycles
    except Exception as e:
        PhoneSELogger.error(f"Failed to get budget cycles: {e}")
        return None

def getBudgetTransactions( budgetId ):
    try :
        budgetCyles = getBudgetCycles(budgetId)
        
        if budgetCyles is None:
            PhoneSELogger.error("Failed to get budget transactions: No budget cycles found")
            return None

        transactions = []
        for budgetCycle in budgetCyles:
            transactions.extend(getBudgetCycleTransactions(budgetCycle))

        return transactions
    except Exception as e:
        PhoneSELogger.error(f"Failed to get budget transactions: {e}")
        return None

def getActiveBudgetCycle( budget : Budget ):
    try :
        # Check if the budget is still active
        currentBudgetCycle = getBudgetCycle(budget.activeBudgetCycleId)
        if currentBudgetCycle is None:
            PhoneSELogger.error("Failed to get active budget cycle: No current budget cycle found")
            return None

        duration = currentBudgetCycle.duration
        startDateOfBudgetCycle = currentBudgetCycle.startDate
        
        if checkIfExpired(startDateOfBudgetCycle, duration, datetime.now()):
            # Budget is expired, create a new budget cycle
            startDateOfNewBudgetCycle = getStartDateOfCurrentCycle(startDateOfBudgetCycle, duration, datetime.now() )

            newBudgetCycle = createBudgetCycle(budget, startDateOfNewBudgetCycle)
            if newBudgetCycle is None:
                PhoneSELogger.error("Failed to get active budget cycle: Failed to create new budget cycle")
                return None

            budget.budgetCycles.append(newBudgetCycle)
            budget.activeBudgetCycleId = newBudgetCycle.id
            return newBudgetCycle

        return currentBudgetCycle
    except Exception as e:
        PhoneSELogger.error(f"Failed to get active budget cycle: {e}")
        return None

def getBudgetCategories( budgetId ):
    try :
        categories = Category.query.filter(Category.budgetId == budgetId).all()
        if categories is None or any(category is None for category in categories):
            PhoneSELogger.error("Failed to get budget categories: No categories found")
            return None

        return categories
    except Exception as e:
        PhoneSELogger.error(f"Failed to get budget categories: {e}")
        return None

def getBudgetAccounts( budgetId ):
    try :
        accounts = Account.query.filter(Account.budgetId == budgetId).all()
        if accounts is None or any(account is None for account in accounts):
            PhoneSELogger.error("Failed to get budget accounts: No accounts found")
            return None

        return accounts
    except Exception as e:
        PhoneSELogger.error(f"Failed to get budget accounts: {e}")
        return None

def getUserBudgets( userId : int ):
    try :
        budgets = Budget.query.filter(Budget.userId == userId).all()
        if budgets is None or any(budget is None for budget in budgets):
            PhoneSELogger.error("Failed to get user budgets: No budgets found")
            return None

        return budgets
    except Exception as e:
        PhoneSELogger.error(f"Failed to get user overall budget: {e}")
        return None

def getUserOverallBudget( userId : int ):
    try :
        user = User.query.filter_by(id=userId).first()
        if user is None : 
            PhoneSELogger.error("User does not exist")
            return None

        budget = getBudget(user.budgetId)

        if budget is None:
            PhoneSELogger.error("Failed to get user overall budget: Budget does not exist")
            return None

        return budget
    except Exception as e:
        PhoneSELogger.error(f"Failed to get user overall budget: {e}")
        return None

def getRelevantBudgets( transaction ) -> Optional[list[Budget]]:
    try :
        categories = transaction.categories
        if categories is None or any(category is None for category in categories):
            PhoneSELogger.error("Failed to get relevant budgets: No categories found")
            return None

        budgetIds = [category.budgetId for category in categories]
        budgets = Budget.query.filter(Budget.id.in_(budgetIds)).all()

        if budgets is None or any(budget is None for budget in budgets):
            PhoneSELogger.error("Failed to get relevant budgets: No budgets found")
            return None

        account = transaction.payer
        if account is None:
            PhoneSELogger.error("Failed to get relevant budgets: Payer account not found")
            return None

        budget = getBudget(account.budgetId)

        if budget is None:
            PhoneSELogger.error("Failed to get relevant budgets: Budget does not exist")
            return None
        
        budgets.append(budget)

        return budgets
    except Exception as e:
        PhoneSELogger.error(f"Failed to get relevant budgets: {e}")
        return None
