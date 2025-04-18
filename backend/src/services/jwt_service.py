import jwt
import os

def verify_token(token: str) -> bool:
    """
    Verify the JWT token.
    """
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False