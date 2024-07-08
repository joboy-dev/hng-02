from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.database import get_db
from app.utilities.exceptions import CustomHTTPException
from app.utilities.response import make_response
from app.utilities import validation, general
from app.api.user import forms, schemas, models, oauth2
from app.api.organisation import models as org_models

auth_router = APIRouter(prefix='/auth', tags=['Authentication'])

@auth_router.post('/register', status_code=status.HTTP_201_CREATED)
def register(schema: schemas.RegisterSchema, db: Session =  Depends(get_db)):
    '''Endpoint for user registration'''

    # Check if user with email already exists
    user = db.query(models.User).filter(models.User.email == schema.email).first()
    if user:
        raise CustomHTTPException(
            detail='Registration unsuccessful',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if password is valid
    if not validation.is_valid_password(schema.password):
        raise CustomHTTPException(
            detail='Registration unsuccessful',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Hash password
    schema.password = validation.hash_password(schema.password)

    # Add user object
    user = models.User(**schema.model_dump())

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create access token for user
    access_token = oauth2.create_access_token(data={'userId': user.userId})

    # Create organisation for user
    organisation = org_models.Organisation(
        name=f"{schema.firstName}'s Organisation",
    )
    db.add(organisation)
    db.commit()
    db.refresh(organisation)

    # Add user to their own organisation
    user.organisations.append(organisation)
    db.commit()

    user_dict = general.convert_model_to_dict(user, fields_to_remove=['password'])

    return make_response(
        status='success',
        message='Registration successful.',
        status_code=status.HTTP_200_OK,
        data={
            'accessToken': access_token,
            'user': user_dict
        }
    )
    

@auth_router.post('/login', status_code=status.HTTP_200_OK)
def login(user_credentials: forms.LoginForm = Depends(), db: Session = Depends(get_db)):
    '''
        Endpoint to log in a user with email and password. An access token will be provided as the response.\n
        Ensure to enter your email in the username field.
        This token will be a bearer token to be used in request headers in this way:\n
            'Authorization': 'Bearer <token>'\n
        'Authorization' is the key and 'Bearer token' will be the value.
    '''
    
    # Check if email exists in database and perform password checks
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user or not validation.verify_password(password=user_credentials.password, hash=user.password):
        raise CustomHTTPException(
            detail='Authentication failed',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Create access token and pass data to be encoded into the token
    access_token = oauth2.create_access_token({'userId': user.userId})

    # Convert user model to dictionary
    user_dict = general.convert_model_to_dict(user, fields_to_remove=['password'])

    return {
        'status': 'success',
        'message': 'Registration successful',
        'data': {
            'accessToken': access_token,
            'user': user_dict
        }
    }
