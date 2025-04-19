from flask import request, Response, json, Blueprint
from typing import Optional, List

from src import db, PhoneSELogger
from src.controllers import (
    account as accountController,
    user as userController,
)
from src.models import (
    Account,
    User,
    Transaction,
)

accountBp = Blueprint('account', __name__)

# POST
@accountBp.route('/create', methods=['POST'])
def createAccount():
    """
    1. Create account object with the details provided in request.
    2. Add the account to the database.
    3. Commit the updated account to database.
    4. If this was unsuccessful, return error. 
       Otherwise, commit account to database and return success.
    """
    try:
        data = request.get_json()
        if not data:
            return Response(json.dumps({"message": "Input data not provided or invalid"}), status=400, mimetype='application/json')
    
        userId : Optional[int]
        try :
            userId = userController.getUserIdFromToken(request.headers['Authorization'])
            if userId is None:
                raise Exception("Invalid token")
        except Exception as e:
            PhoneSELogger.error(f"Failed to create account: {e}")
            return Response(json.dumps({"message": "Failed to create account", "error": str(e)}), status=500, mimetype='application/json')
        

        account: Optional[Account]
        try:
            account = accountController.createAccount(userId, **data)
            if account is None:
                raise Exception("Failed to create account object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to create account: {e}")
            return Response(json.dumps({"message": "Failed to create account", "error": str(e)}), status=500, mimetype='application/json')

        db.session.add(account)
        db.session.commit()

        return Response(json.dumps({"message": "Account created successfully"}), status=200, mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        PhoneSELogger.error(f"Failed to create account: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

# GET
@accountBp.route('/get/<int:id>', methods=['GET'])
def getAccount(id: int):
    """
    1. Get account object from database.
    2. If this was unsuccessful, return error.
       Otherwise, return account.
    """
    try:
        account: Optional[Account]
        try:
            account = accountController.getAccount(id)
            if account is None:
                raise Exception("Failed to get account object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get account: {e}")
            return Response(json.dumps({"message": "Failed to get account", "error": str(e)}), status=500, mimetype='application/json')

        response = json.jsonify(account)
        return response

    except Exception as e:
        PhoneSELogger.error(f"Failed to get account: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

# GET
@accountBp.route('/getDetails/<int:id>', methods=['GET'])
def getAccountDetails(id: int):
    """
    1. Get account object from database.
    2. If this was unsuccessful, return error.
       Otherwise, return account.
    """
    try:
        account: Optional[Account]
        try:
            account = accountController.getAccountDetails(id)
            if account is None:
                raise Exception("Failed to get account object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get account: {e}")
            return Response(json.dumps({"message": "Failed to get account", "error": str(e)}), status=500, mimetype='application/json')

        response = json.jsonify(account)
        return response

    except Exception as e:
        PhoneSELogger.error(f"Failed to get account: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

# PUT
@accountBp.route('/update/<int:id>', methods=['PUT'])
def updateAccount(id: int):
    """
        Update the given attributes of the account.
    """
    try:
        data = request.get_json()
        if not data:
            return Response(json.dumps({"message": "Input data not provided or invalid"}), status=400, mimetype='application/json')

        account: Optional[Account]
        try:
            account = accountController.updateDetails(id, **data)
            if account is None:
                raise Exception("Failed to update account object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to update account: {e}")
            return Response(json.dumps({"message": "Failed to update account", "error": str(e)}), status=500, mimetype='application/json')

        response = json.jsonify(account)
        return response

    except Exception as e:
        PhoneSELogger.error(f"Failed to update account: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

@accountBp.route('/balance/<int:id>', methods=['GET'])
def getBalance(id: int):
    try:
        balance: Optional[float]
        try:
            balance = accountController.getAccountBalance(id)
            if balance is None:
                raise Exception("Failed to get balance object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get balance: {e}")
            return Response(json.dumps({"message": "Failed to get balance", "error": str(e)}), status=500, mimetype='application/json')

        response = json.jsonify(balance)
        return response

    except Exception as e:
        PhoneSELogger.error(f"Failed to get balance: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

@accountBp.route('/delete/<int:id>', methods=['DELETE'])
def deleteAccount(id: int):
    try:
        account: Optional[Account]
        try:
            account = accountController.deleteAccount(id)
            if account is None:
                raise Exception("Failed to delete account object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to delete account: {e}")
            return Response(json.dumps({"message": "Failed to delete account", "error": str(e)}), status=500, mimetype='application/json')

        response = json.jsonify(account)
        return response

    except Exception as e:
        PhoneSELogger.error(f"Failed to delete account: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')


@accountBp.route('/getTransactions/<int:id>', methods=['GET'])
def getAccountTransactions(id: int):
    """
        Returns the transactions of the account
    """
    try:
        try:
            transactions = accountController.getAccountTransactions(id)
            if transactions is None:
                raise Exception("Failed to get account object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get account: {e}")
            return Response(json.dumps({"message": "Failed to get account", "error": str(e)}), status=500, mimetype='application/json')

        response = json.jsonify({"transactions": transactions})
        return response

    except Exception as e:
        PhoneSELogger.error(f"Failed to get account: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

@accountBp.route('/setBalance/<int:id>', methods=['PATCH'])
def setBalance(id: int):
    """
        Set the balance of the account
    """
    try:
        data = request.get_json()
        if not data:
            return Response(json.dumps({"message": "Input data not provided or invalid"}), status=400, mimetype='application/json')

        account: Optional[Account]
        try:
            account = accountController.setAccountBalance(id, **data)
            if account is None:
                raise Exception("Failed to update account object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to update account: {e}")
            return Response(json.dumps({"message": "Failed to update account", "error": str(e)}), status=500, mimetype='application/json')

        response = json.jsonify(account)
        return response

    except Exception as e:
        PhoneSELogger.error(f"Failed to update account: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

@accountBp.route('/credit/<int:id>', methods=['PATCH'])
def creditAccount(id: int):
    """
        Set the balance of the account
    """
    try:
        data = request.get_json()
        if not data:
            return Response(json.dumps({"message": "Input data not provided or invalid"}), status=400, mimetype='application/json')

        account: Optional[Account]
        try:
            account = accountController.creditAccount(id, **data)
            if account is None:
                raise Exception("Failed to update account object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to update account: {e}")
            return Response(json.dumps({"message": "Failed to update account", "error": str(e)}), status=500, mimetype='application/json')

        response = json.jsonify(account)
        return response

    except Exception as e:
        PhoneSELogger.error(f"Failed to update account: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

@accountBp.route('/debit/<int:id>', methods=['PATCH'])
def debitAccount(id: int):
    """
        Set the balance of the account
    """
    try:
        data = request.get_json()
        if not data:
            return Response(json.dumps({"message": "Input data not provided or invalid"}), status=400, mimetype='application/json')

        account: Optional[Account]
        try:
            account = accountController.debitAccount(id, **data)
            if account is None:
                raise Exception("Failed to update account object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to update account: {e}")
            return Response(json.dumps({"message": "Failed to update account", "error": str(e)}), status=500, mimetype='application/json')

        response = json.jsonify(account)
        return response

    except Exception as e:
        PhoneSELogger.error(f"Failed to update account: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

@accountBp.route('/getByUser', methods=['GET'])
def getUserAccounts():
    """
        Returns the transactions of the account
    """
    try:
        userId = int
        try:
            userId = userController.getUserIdFromToken(request.headers['Authorization'])
            if userId is None:
                raise Exception("Invalid token")

            accounts = accountController.getUserAccounts(userId)
            if accounts is None:
                raise Exception("Failed to get account object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get account: {e}")
            return Response(json.dumps({"message": "Failed to get account", "error": str(e)}), status=500, mimetype='application/json')

        response = json.jsonify({"accounts": accounts})
        return response

    except Exception as e:
        PhoneSELogger.error(f"Failed to get account: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')
