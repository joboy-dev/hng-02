from app.api.organisation.models import Organisation

def test_register(client, test_db):
    '''Test for register endpoint'''

    response = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@gmail.com",
        "password": "Johndoe@123",
        "phone": '0904712346'
    })

    # Check status code
    assert response.status_code == 201
    data = response.json()

    assert data["status"] == "success"
    # Check for access token
    assert "accessToken" in data["data"]

    # Check for user details
    assert data["data"]["user"]["firstName"] == "John"
    assert data["data"]["user"]["lastName"] == "Doe"

    # Check for organisation existence
    org = test_db.query(Organisation).filter(Organisation.name == "John's Organisation").first()
    assert org


def test_missing_fields(client):
    '''Test for missing fields in register endpoint'''

    miss_firstname_res = client.post("/auth/register", json={
        "lastName": "Doe",
        "email": "john.doe@gmail.com",
        "password": "Johndoe@123",
        "phone": '0904712346'
    })
    assert miss_firstname_res.status_code == 422
    assert miss_firstname_res.json()['errors'][0]['field'] == 'firstName'
    assert miss_firstname_res.json()['errors'][0]['message'] == 'Field required'

    miss_lastname_res = client.post("/auth/register", json={
        "firstName": "John",
        "email": "john.doe@gmail.com",
        "password": "Johndoe@123",
        "phone": '0904712346'
    })
    assert miss_lastname_res.status_code == 422
    assert miss_lastname_res.json()['errors'][0]['field'] == 'lastName'
    assert miss_lastname_res.json()['errors'][0]['message'] == 'Field required'

    miss_email_res = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "password": "Johndoe@123",
        "phone": '0904712346'
    })
    assert miss_email_res.status_code == 422
    assert miss_email_res.json()['errors'][0]['field'] == 'email'
    assert miss_email_res.json()['errors'][0]['message'] == 'Field required'

    miss_password_res = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@gmail.com",
        "phone": '0904712346'
    })
    assert miss_password_res.status_code == 422
    assert miss_password_res.json()['errors'][0]['field'] == 'password'
    assert miss_password_res.json()['errors'][0]['message'] == 'Field required'


def test_reegister_duplicate_email(client, test_db):
    '''Test for register endpoint'''

    response = client.post("/auth/register", json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@gmail.com",
        "password": "Johndoe@123",
        "phone": '0904712346'
    })

    # Check status code
    assert response.status_code == 400
    assert response.json()['message'] == 'Registration unsuccessful'


def test_login(client, test_db):
    '''Test for login endpoint'''

    success_response = client.post("/auth/login", data={
        "email": "john.doe@gmail.com",
        "password": "Johndoe@123",
    })

    error_response = client.post("/auth/login", data={
        "email": "john.doe1@gmail.com",
        "password": "Johndoe@123",
    })

    assert success_response.status_code == 200
    assert error_response.status_code == 400
