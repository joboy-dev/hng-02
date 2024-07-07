import re
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.utilities.exceptions import CustomHTTPException
from app.utilities.response import make_response

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def is_valid_password(password: str) -> bool:
    '''Function to check if password is valid'''
    
    # Regular expression for a valid password
    # Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, one digit, and one special character.
    password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    
    return True if re.match(password_regex, password) else False
    

def hash_password(password: str) -> str:
    '''Function to hash a password'''
    
    hashed_password = pwd_context.hash(secret=password)     
    return hashed_password


def verify_password(password: str, hash: str) -> bool:
    '''Function to verify a hashed password'''
    
    return pwd_context.verify(secret=password, hash=hash) 


def check_model_existence(db, model, model_id):
    '''Function to check if a model exists'''
    
    model_obj = db.get(model, ident=model_id)
    
    if not model_obj:    
        raise CustomHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{model.__name__} not found'
        )
    
    return model_obj
