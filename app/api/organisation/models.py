import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.database import Base
from app.utilities.general import generate_id

# Define an association table for members of an organization to create a many-to-many association between users and organisations
user_organisation = sa.Table(
    'user_organisation', 
    Base.metadata,
    sa.Column('user_id', sa.String, sa.ForeignKey('users.user_id'), primary_key=True),
    sa.Column('organisation_id', sa.String, sa.ForeignKey('organisations.org_id'), primary_key=True)
)


class Organisation(Base):
    '''Organisation table model'''
    __tablename__ = 'organisations'

    org_id = sa.Column(sa.String, primary_key=True, default=generate_id)
    name = sa.Column(sa.String, index=True, nullable=False)
    description = sa.Column(sa.String, nullable=True)

    members = relationship('User', secondary=user_organisation, back_populates='organisations')
