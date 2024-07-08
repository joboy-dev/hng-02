from time import sleep

import pytest
from app.api.user.models import User
from app.api.organisation.models import Organisation
from app.api.user.oauth2 import create_access_token, decode_token

def test_token_generation(client, test_db):
    '''Test for token generation'''

    user = User(
        email='test@gmail.com',
        password='Korede@036',
        firstName='Test',
        lastName='User',
        phone='08012345678'
    )

    # Add user to test database
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    # Create and decode access token
    token = create_access_token({'userId': user.userId})
    decoded_token = decode_token(token)

    assert decoded_token['userId'] == user.userId
    assert 'exp' in decoded_token


def test_token_expiration(client):
    '''Test for token expiration'''
    
    token = create_access_token(data={"user_id": "someid"}, hours=0.001)
    sleep(5)
    with pytest.raises(Exception):
        decode_token(token)


def test_organisation_access(client, test_db):
    '''Test for organization access'''

    # Create users
    user1 = User(
        email='test1@gmail.com',
        password='Korede@036',
        firstName='Test',
        lastName='User1',
        phone='08012345678'
    )

    user2 = User(
        email='test2@gmail.com',
        password='Korede@036',
        firstName='Test',
        lastName='User2',
        phone='08012345678'
    )
    test_db.add(user1)
    test_db.add(user2)
    test_db.commit()

    # Create organisation for user1
    organisation = Organisation(name="User1 Org")
    test_db.add(organisation)
    test_db.commit()

    # Add organisation to user1's organisation list
    user1.organisations.append(organisation)
    test_db.commit()

    # create access token foruser 2
    access_token = create_access_token(data={"userId": user2.userId})
    
    # Try to access user1's organisation with user2's token
    response = client.get(
        f"/api/organisations/{organisation.orgId}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 400
    assert response.json()["message"] == "You are not a member of this organisation"
