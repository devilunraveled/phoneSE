from typing import Optional

from src import PhoneSELogger

from src.models.budget import Budget
from src.models.budgetCycle import BudgetCycle
from src.models.transaction import Transaction

from src.controllers.user import checkIfUserExists
from src.controllers.budgetCycle import createBudgetCycle, getBudgetCycleTransactions

# POst
def createBudget( name, userId, createTime, duration = None, description = None ) ->Optional[Budget]:
    # Check if the user exists
    if not checkIfUserExists( userId ):
        PhoneSELogger.error( "Budget creation failed: User does not exist" )
        return None

    try:
        if description is None:
            description = ""

        PhoneSELogger.info(f"Creating budget: {name}")
        budget = Budget(
                name=name, 
                userId=userId, 
                duration=duration, 
                description=description,
                creationDate=createTime)

        PhoneSELogger.info(f"Budget created: {budget}")
        return budget
    except Exception as e:
        PhoneSELogger.error(f"Failed to create budget: {e}")
        return None

# DELETE
def deleteBudget(budgetId : int):
    try :
        PhoneSELogger.info(f"Deleting budget: {budgetId}")
        budget = getBudget(budgetId)
        
        if budget is None:
            PhoneSELogger.warning("Budget deletion failed: Budget does not exist")
            return None

        return budget
    except Exception as e:
        PhoneSELogger.error(f"Failed to delete budget: {e}")
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
        
        # Make current active budget cycle inactive
        currentActiveBudgetCycle : BudgetCycle = getActiveBudgetCycle(budget)
        currentActiveBudgetCycle.makeInactive()
        
        # Make the new cycle active.
        newBudgetCycle : BudgetCycle = createBudgetCycle(budget)
        newBudgetCycle.makeActive()

        budget.budgetCycles.append(newBudgetCycle)

        return newBudgetCycle

    except Exception as e:
        PhoneSELogger.error(f"Failed to create new budget cycle: {e}")
        return None
        

def getBudgetCycles( budgetId ) -> Optional[list[BudgetCycle]]:
    try :
        budgetCycles = BudgetCycle.query.filter_by(budgetId=budgetId).all()
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
    pass

def getBudgetCategories():
    pass
