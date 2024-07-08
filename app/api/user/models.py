import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.utilities.general import generate_id
from app.database import Base
from app.api.organisation.models import user_organisation

class User(Base):
    '''User table model'''

    __tablename__ = 'users'

    userId = sa.Column(sa.String, primary_key=True, default=generate_id, unique=True)
    firstName = sa.Column(sa.String, nullable=False)
    lastName = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, unique=True, index=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    phone = sa.Column(sa.String, nullable=True)
    
    organisations = relationship('Organisation', secondary=user_organisation, back_populates='members')
