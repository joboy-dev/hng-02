from fastapi import status
from app.api.organisation.models import Organisation
from app.api.user.models import User
from app.utilities.exceptions import CustomHTTPException


def is_organization_member(user: User, organisation: Organisation):
    '''Permission to check if a user is a member of an organisation'''

    if user not in organisation.members:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You are not a member of this organisation', 
        )
    

