# from tests.conftest import test_db, client
from app.api.user.models import User
from app.api.user.oauth2 import create_access_token, verify_access_token

# c = client()
# db = test_db()

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
    decoded_token = verify_access_token(token)

    assert decoded_token['id'] == user.userId
    assert 'exp' in decoded_token

    




# E2E Tests