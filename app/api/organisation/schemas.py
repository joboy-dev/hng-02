from typing import List
from pydantic import BaseModel

# from app.api.user.schemas import BaseUserResponse


class BaseOrganisationResponse(BaseModel):
    '''Base response schema for organisations'''

    org_id: str
    name: str
    description: str | None


# class OrganisationWithMembersResponse(BaseOrganisationResponse):
#     '''Organisation with members response schema for organisations'''

#     members: List[BaseUserResponse]

#     class Config:
#         orm_mode = True


class CreateOrganisation(BaseModel):
    '''Schema for creating organisations'''

    name: str
    description: str | None


class AddUserToOrganisation(BaseModel):
    '''Schema for adding users to organisations'''

    user_id: str
    