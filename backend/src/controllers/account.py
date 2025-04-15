from src import db

from backend.src.models.account import Account

from src.controllers.user import checkIfUserExists

#POST
def createAccount( userID, name, *args, **kwargs ):
    """
        Creates a new account for the user
    """
    
    # Check if user exists
    if not checkIfUserExists( userID ):
        return False # Possibly raise an exception here.

    # Create account
    # ! add try catch here
    newAccount = Account( userID = userID, name = name )
    db.session.add( newAccount )
    db.session.commit()

    return True
