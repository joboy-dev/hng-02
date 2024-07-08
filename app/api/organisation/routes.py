from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session

from app.database import get_db
from app.utilities.exceptions import CustomHTTPException
from app.utilities.response import make_response
from app.utilities import general, validation
from app.api.user import models as user_models, oauth2
from app.api.organisation import models, schemas, permissions

org_router = APIRouter(prefix='/api/organisations', tags=['Organisation'])

@org_router.get('', status_code=status.HTTP_200_OK)
def get_all_user_organiations(db: Session = Depends(get_db), current_user: user_models.User = Depends(oauth2.get_current_user)):
    '''Endpoint to get all organizations of the current user'''

    user_organisations = current_user.organisations

    return make_response(
        status_code=status.HTTP_200_OK,
        status='success', 
        message='Organisations retrieved successfully', 
        data={
            'organisations': [general.convert_model_to_dict(organisation) for organisation in user_organisations]
        }
    )


@org_router.post('', status_code=status.HTTP_201_CREATED)
def create_organisation(schema: schemas.CreateOrganisation, db: Session = Depends(get_db), current_user: user_models.User = Depends(oauth2.get_current_user)):
    '''Endpoint to get all organizations of the current user'''

    # Create organization
    organisation = models.Organisation(**schema.model_dump())
    db.add(organisation)
    db.commit()
    db.refresh(organisation)

    # Add current user to user_organisation table
    current_user.organisations.append(organisation)
    db.commit()

    return make_response(
        status_code=status.HTTP_201_CREATED,
        status='success', 
        message='Organisation created successfully', 
        data=general.convert_model_to_dict(organisation)
    )


@org_router.get('/{orgId}', status_code=status.HTTP_200_OK)
def get_single_organisation(orgId: str, db: Session = Depends(get_db), current_user: user_models.User = Depends(oauth2.get_current_user)):
    '''Endpoint to get all organizations of the current user'''

    # Check if organisation exists
    organisation = validation.check_model_existence(db, models.Organisation, orgId)
    
    # Check if current logged in user is not in the organisation's members to restrict access
    permissions.is_organization_member(user=current_user, organisation=organisation)

    return make_response(
        status_code=status.HTTP_200_OK,
        status='success', 
        message='Organisation retrieved successfully', 
        data=general.convert_model_to_dict(organisation)
    )


@org_router.post('/{orgId}/users', status_code=status.HTTP_200_OK)
def add_user_to_organisation(schema: schemas.AddUserToOrganisation, orgId: str, db: Session = Depends(get_db), current_user: user_models.User = Depends(oauth2.get_current_user)):
    '''Endpoint to add user to organization'''

    # Check if organisation exists
    organisation = validation.check_model_existence(db, models.Organisation, orgId)
    
    # Check if user exists
    user = validation.check_model_existence(db, user_models.User, schema.userId)
    
    # Check if current logged in user is not in the organisation's members to restrict access
    permissions.is_organization_member(user=current_user, organisation=organisation)
    
    # Check if user is already in organisation
    if user in organisation.members:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already in organisation'
        )
    
    # Add user to organisation memebers
    organisation.members.append(user)
    db.commit()

    return make_response(
        status_code=status.HTTP_200_OK,
        status='success', 
        message='User added to organisation successfully'
    )
