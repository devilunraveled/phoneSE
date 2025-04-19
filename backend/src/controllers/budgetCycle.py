from typing import Optional

from src import PhoneSELogger
from src.models.budgetCycle import BudgetCycle
from src.models.budget import Budget

def getBudgetCycle( budgetCycleId : int ) -> Optional[BudgetCycle]:
    try :
        PhoneSELogger.info(f"Getting budget cycle: {budgetCycleId}")
        budgetCycle = BudgetCycle.query.get(budgetCycleId)
        return budgetCycle
    except Exception as e:
        PhoneSELogger.error(f"Failed to get budget cycle: {e}")
        return None

def createBudgetCycle( budget : Budget, startDate ) -> Optional[BudgetCycle]:
    try :
        PhoneSELogger.info(f"Creating budget cycle: {budget}")
        budgetCycle = BudgetCycle(amount = budget.amount, 
                                  currency = budget.currency, 
                                  startDate = startDate, 
                                  endDate = startDate + budget.duration, 
                                  budgetId = budget.id )
        return budgetCycle
    except Exception as e:
        PhoneSELogger.error(f"Failed to create budget cycle: {e}")
        return None

def getBudgetCycleTransactions():
    try :
        PhoneSELogger.info("Getting budget cycle transactions")
        return None
    except Exception as e:
        PhoneSELogger.error(f"Failed to get budget cycle transactions: {e}")
        return None
