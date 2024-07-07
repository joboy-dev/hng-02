from typing import List, Optional
from pydantic import BaseModel, EmailStr

from app.api.organisation.schemas import BaseOrganisationResponse


class BaseUserResponse(BaseModel):
    '''Base response schema for users'''

    user_id: str
    email: EmailStr
    first_name: str
    last_name: str
    phone: str | None

    class Config:
        orm_mode = True


class UserWithOrganisationsResponse(BaseModel):
    '''Complete user response with organisations information'''

    organisations: List[BaseOrganisationResponse]

    class Config:
        orm_mode = True


class RegisterSchema(BaseModel):
    '''User registration schema'''

    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str | None = None


class LoginSchema(BaseModel):
    '''User login schema'''

    email: EmailStr
    password: str


class TokenData(BaseModel):
    '''Schema to structure token data'''
    
    id: Optional[str]
    