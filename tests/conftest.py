import pytest
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app.settings import settings
from app.models import Post, Vote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = f"{settings.DATABASE_URL}_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    data = {'email': 'test@example.com', 'password': 'test'}
    response = client.post('/users', json=data)
    assert response.status_code == 201
    user = response.json()
    user['password'] = data['password']
    return user


@pytest.fixture()
def test_user2(client):
    data = {'email': 'test@example2.com', 'password': 'test'}
    response = client.post('/users', json=data)
    assert response.status_code == 201
    user = response.json()
    user['password'] = data['password']
    return user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f"Bearer {token}"
    }
    return client


@pytest.fixture
def create_post(authorized_client):
    response = authorized_client.post('/posts', json={
        'title': 'ASDADKA',
        'content': 'SDKADK'
    })
    return response


@pytest.fixture
def test_posts(test_user, session, test_user2):
    data = [
        {
            'title': 'title 01',
            'content': 'content 01',
            'author_id': test_user['id']
        },
        {
            'title': 'title 02',
            'content': 'content 02',
            'author_id': test_user['id']
        },
        {
            'title': 'title 03',
            'content': 'content 03',
            'author_id': test_user['id']
        },
        {
            'title': 'title 04',
            'content': 'content 04',
            'author_id': test_user['id']
        },
        {
            'title': 'title 05',
            'content': 'content 05',
            'author_id': test_user2['id']
        }
    ]

    def create_post_model(post):
        return Post(**post)

    formated_posts = list(map(create_post_model, data))
    session.add_all(formated_posts)
    session.commit()

    posts = session.query(Post).all()
    return posts


@pytest.fixture
def test_vote(test_posts, test_user, session):
    new_vote = Vote(
        post_id=test_posts[0].id,
        author_id=test_user['id']
    )
    session.add(new_vote)
    session.commit()
