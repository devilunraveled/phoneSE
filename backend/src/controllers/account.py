from src import db

from src.models.accountModel import Account

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
    newAccount = Account( userID = userID, name = name )
    db.session.add( newAccount )
    db.session.commit()

    return True
