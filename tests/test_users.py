import pytest
from app import schemas
from jose import jwt
from app.settings import settings


def test_get_all_users(client):
    response = client.get('/users')
    assert response.status_code == 200


def test_create_user(client):
    response = client.post('/users/', json={
        'email': '12345@12345.com',
        'password': 'teste'
    })
    user = schemas.UserPublic(**response.json())
    assert user.email == '12345@12345.com'
    assert response.json().get('email') == '12345@12345.com'
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post('/login', data={
        'username': test_user['email'],
        'password': test_user['password'],
    })

    login_response = schemas.Token(**response.json())

    data = jwt.decode(login_response.access_token,
                      settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print(
        f"DATA -> {data}, USER -> {test_user}, RESPONSE -> {response.json()}")
    id = data.get('user_id')
    assert id == test_user['id']
    assert login_response.token_type == 'bearer'
    assert response.status_code == 200


def test_get_user_by_id(client, test_user):
    response = client.get(f'/users/{test_user["id"]}')
    assert response.status_code == 200


def test_get_user_by_wrong_id(client):
    response = client.get(f'/users/100')
    assert response.status_code == 404
    assert response.json().get(
        'detail') == f'User with id 100 not exists'


@pytest.mark.parametrize('email, password, status_code', [
    ('wrong@email.com', 'test', 403),
    ('test@example.com', 'wrong_password', 403)
])
def test_incorrect_login(client, email, password, status_code):
    response = client.post('/login', data={
        'username': email,
        'password': password
    })

    assert response.status_code == status_code
