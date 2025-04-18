from typing import Optional
from src.models.account import Account
from src.models.transaction import Transaction

from src.controllers.user import checkIfUserExists
from src import PhoneSELogger

# GET
def getAccount( accountId ) -> Optional[Account]:
    try :
        PhoneSELogger.info( "Fetching account" )
        account = Account.query.get( accountId )
        return account
    except Exception as e:
        PhoneSELogger.error( "Account fetch failed: " + str(e) )
        return None

def getAccountBalance( accountId ) -> Optional[float]:
    try :
        account = getAccount( accountId )

        if account is None:
            PhoneSELogger.error( "Account balance fetch failed: Account does not exist" )
            return None

        PhoneSELogger.debug( f"{account.name} account balance fetched successfully : {account.balance}" )
        return account.balance
    except Exception as e:
        PhoneSELogger.error( "Account balance fetch failed: " + str(e) )
        return None

def getAccountDetails( accountId ):
    try :
        account = getAccount( accountId )

        if account is None:
            PhoneSELogger.error( "Account details fetch failed: Account does not exist" )
            return None

        PhoneSELogger.debug( f"{account.name} account details fetched successfully" )
        return account
    except Exception as e:
        PhoneSELogger.error( "Account details fetch failed: " + str(e) )
        return None

def getAccountTransactions( accountId ) -> Optional[list[Transaction]]:
    try :
        PhoneSELogger.info( "Fetching account transactions" )
        query = Transaction.payer == accountId or Transaction.payee == accountId
        transactions = Transaction.query.filter( query ).all()

        if transactions is None:
            PhoneSELogger.error( "Account transactions fetch failed: No transactions found" )
            return None

        PhoneSELogger.debug( f"{len(transactions)} account transactions fetched successfully" )
        return transactions
    except Exception as e:
        PhoneSELogger.error( "Account transactions fetch failed: " + str(e) )
        return None

def getAccountBudget( accountId ): # TO Discuss
    try :
        PhoneSELogger.info( "Fetching account budgets" )
        account = getAccount( accountId )

        if account is None:
            PhoneSELogger.error( "Account budgets fetch failed: Account does not exist" )
            return None

        if account.budget is None:
            PhoneSELogger.warning( "Account budgets fetch failed: No budgets found" )
            return None

        PhoneSELogger.debug( f"{account.name} account budgets fetched successfully" )
        return account.budget

    except Exception as e:
        PhoneSELogger.error( "Account budgets fetch failed: " + str(e) )
        return None

#POST
def createAccount( userId, name, *args, **kwargs ):
    """
        Creates a new account for the user
    """
    
    # Check if user exists
    if not checkIfUserExists( userId ):
        PhoneSELogger.error( "Account creation failed: User does not exist" )
        return None

    # Create account
    try :
        newAccount = Account( userId = userId, name = name, *args, **kwargs )
        PhoneSELogger.info( "Account created successfully" )
        return newAccount
    except Exception as e:
        PhoneSELogger.error( "Account creation failed: " + str(e) )
        return None

#PATCH
def updateDetails( accountID, **kwargs ):
    """
        Create the details for an account :
        name, description.
    """
    try :
        account = getAccount( accountID )

        if account is None:
            PhoneSELogger.error( "Account details update failed: Account does not exist" )
            return None

        for key, value in kwargs.items(): #?? Unsafe as it is.
            if not hasattr( account, key ):
                PhoneSELogger.error(f"Account details update failed: Invalid attribute : {key}")
                return None
            setattr( account, key, value )
            PhoneSELogger.debug(f"Account details updated: {key} : {value}")

        PhoneSELogger.info( "Account details updated successfully" )
        return account
    except Exception as e:
        PhoneSELogger.error( "Account details update failed: " + str(e) )
        return None

def setAccountBalance( accountId, balance, currency = None):
    """
        Set the balance for an account
    """
    try :
        if balance < 0 :
            PhoneSELogger.warning( "Account balance being made negative" )

        account = getAccount( accountId )
        
        if account is None:
            PhoneSELogger.error( "Account balance update failed: Account does not exist" )
            return None

        account.balance = balance
        
        if currency is not None and account.currency != currency:
            account.currency = currency

        PhoneSELogger.info( "Account balance updated successfully" )
        return account
    except Exception as e:
        PhoneSELogger.error( "Account balance update failed: " + str(e) )
        return None

def creditAccount( accountId, credit, currency = None):
    """
        Add funds to an account
    """
    try :
        if credit < 0 :
            PhoneSELogger.warning( "Account balance update failed: Credit cannot be negative." )

        account = getAccount( accountId )
        
        if account is None:
            PhoneSELogger.error( "Account balance update failed: Account does not exist" )
            return None

        if currency is not None and account.currency != currency:
            PhoneSELogger.error( f"Account balance update failed: Currency mismatch - {account.currency} != {currency} " )
            return None

        account.balance += credit
        
        PhoneSELogger.info( "Account balance updated successfully" )
        return account
    except Exception as e:
        PhoneSELogger.error( "Account balance update failed: " + str(e) )
        return None

def debitAccount( accountId, debit, currency = None):
    try :
        if debit < 0 :
            PhoneSELogger.warning( "Account balance update failed: Debit cannot be negative." )

        account = getAccount( accountId )

        if account is None :
            PhoneSELogger.error( "Account balance update failed: Account does not exist" )
            return None

        if currency is not None and account.currency != currency:
            PhoneSELogger.error( f"Account balance update failed: Currency mismatch - {account.currency} != {currency} " )
            return None

        if account.balance < debit:
            PhoneSELogger.error( "Account balance update failed: Insufficient funds" )
            return None

        account.balance -= debit

        PhoneSELogger.info( "Account balance updated successfully" )
        return account
    except Exception as e:
        PhoneSELogger.error( "Account balance update failed: " + str(e) )
        return None

def deleteAccount( accountId ):
    try :
        account = getAccount( accountId )

        if account is None:
            PhoneSELogger.error( "Account deletion failed: Account does not exist" )
            return None

        return account
    except Exception as e:
        PhoneSELogger.error( "Account deletion failed: " + str(e) )
        return None
