from app.api.user.models import User
from app.api.organisation.models import Organisation
from app.api.user.oauth2 import create_access_token, decode_token

# Unit Tests
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


def test_organisation_access(client, test_db):
    '''Test for organization access'''

    # Create user
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

    organisation = Organisation(name="User1 Org")
    test_db.add(organisation)
    test_db.commit()

    user1.organisations.append(organisation)
    test_db.commit()

    access_token = create_access_token(data={"userId": user2.userId})
    
    response = client.get(
        f"/api/organisations/{organisation.orgId}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 400
    assert response.json()["message"] == "You are not a member of this organisation"




# End-to-End Tests