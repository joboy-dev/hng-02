import datetime as dt
import uuid

from fastapi import HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.config import settings
from app.api.user import models, schemas
from app.database import get_db
from app.utilities.exceptions import CustomHTTPException
from app.utilities.response import make_response

oauth2_scheme = OAuth2PasswordBearer('/auth/login')

def create_access_token(data: dict) -> str:
    '''Function to create access tpken'''
    
    data_to_encode = data.copy()
    
    expires = dt.datetime.now(dt.UTC) + dt.timedelta(hours=settings.access_token_expire_hours)
    data_to_encode.update({
        'exp': expires,
        'type': 'access'
    })
    
    encoded_jwt = jwt.encode(data_to_encode, settings.secret_key, settings.algorithm)
    return encoded_jwt


def verify_access_token(access_token: str, credentials_exception):
    '''Funtcion to decode and verify access token'''
    
    try:
        payload = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: uuid.UUID = payload.get('user_id')
        
        if user_id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=user_id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    '''Function to get current logged in user''' 
    
    credentials_exception = CustomHTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Authentication failed',
        headers={'WWW-Authenticate': 'Bearer'}
    )   
    
    token = verify_access_token(access_token, credentials_exception)
    user =  db.query(models.User).filter(models.User.user_id == token.id).first()
    
    return user
