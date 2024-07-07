from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session

from app.database import get_db
from app.utilities.exceptions import CustomHTTPException
from app.utilities.response import make_response
from app.utilities import general, validation
from app.api.user import models, oauth2

user_router = APIRouter(prefix='/api/users', tags=['Users'])

@user_router.get('', status_code=status.HTTP_200_OK)
def get_user_profile(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    '''Endpoint to get details of logged in user'''

    user_dict = general.convert_model_to_dict(current_user, fields_to_remove=['password'])

    return make_response(
        status_code=status.HTTP_200_OK,
        status='success',
        message='User details retrieved successfully',
        data=user_dict
    )


@user_router.get('/{id}', status_code=status.HTTP_200_OK)
def get_user_by_id(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    '''Endpoint to get details of a user'''

    # Check if user exists
    user = validation.check_model_existence(db, models.User, id)
        
    # Check if user is in an organisation common to themselves
    user_in_org = False
    for org in current_user.organisations:
        if user in org.members:
            user_in_org = True
            break
    
    if not user_in_org:
        raise CustomHTTPException(
            detail='User does not belong to any organisation as yourself',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user_dict = general.convert_model_to_dict(user, fields_to_remove=['password'])

    return make_response(
        status_code=status.HTTP_200_OK,
        status='success',
        message='User details retrieved successfully',
        data=user_dict
    )
    
