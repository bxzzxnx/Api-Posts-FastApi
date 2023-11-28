from app import schemas
import pytest


def test_get_authorized_posts(authorized_client, create_post):
    response = authorized_client.get('/posts/')
    assert response.status_code == 200


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get('/posts')
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)


def test_unauthorized_get_posts(client):
    response = client.get('/posts')
    assert response.status_code == 401
    assert response.json().get('detail') == 'Not authenticated'


def test_unauthorized_get_post_by_id(client, test_posts):
    response = client.get(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401


def test_get_one_post_not_exists(authorized_client):
    response = authorized_client.get('/posts/100')
    assert response.status_code == 404
    assert response.json().get('detail') == 'Não encontrado'


def test_authorized_get_post_by_id(authorized_client, test_posts):
    TEST_POST = test_posts[0]
    response = authorized_client.get(f'/posts/{TEST_POST.id}')
    post = schemas.PostOut(**response.json())
    assert post.Post.title == TEST_POST.title
    assert post.Post.id == TEST_POST.id
    assert response.status_code == 200


@pytest.mark.parametrize('title, content, published', [
    ('title 100', 'content 100', True),
    ('title 200', 'content 200', False),
    ('title 300', 'content 300', True)
])
def test_create_post(authorized_client, title, content, published):
    response = authorized_client.post('/posts', json={
        'title': title,
        'content': content,
        'published': published
    })

    post = schemas.Post(**response.json())
    assert response.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published


def test_create_post_default_published(authorized_client, test_user):
    response = authorized_client.post('/posts', json={
        'title': 'title',
        'content': 'content'
    })

    post = schemas.Post(**response.json())
    assert post.author_id == test_user['id']
    assert post.published == True
    assert response.status_code == 201


def test_unauthorized_create_post(client):
    response = client.post('/posts', json={
        'title': 'title',
        'content': 'content'
    })

    assert response.status_code == 401


def test_unauthorized_delete_post(client, test_posts):
    response = client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401


def test_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 204


def test_delete_invalid_post(authorized_client):
    response = authorized_client.delete('/posts/100')
    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    response = authorized_client.delete(f'/posts/{test_posts[-1].id}')
    assert response.status_code == 403  # Forbidden
    print(response)


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[0].id
    }
    response = authorized_client.put(f'/posts/{test_posts[0].id}', json=data)

    updated_post = schemas.Post(**response.json())

    assert response.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.author_id == data['id']


def test_update_another_user_post(authorized_client, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[4].id
    }

    response = authorized_client.put(f'/posts/{test_posts[4].id}', json=data)
    assert response.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    data = {
        'title': 'updated title',
        'content': 'updated content',
        'id': test_posts[0].id
    }

    response = client.put(f'/posts/{test_posts[0].id}', json=data)
    assert response.status_code == 401  # unauthorized


def test_update_test_with_nothing_pass(authorized_client, test_posts):
    response = authorized_client.put(f'/posts/{test_posts[0].id}')
    assert response.status_code == 422  # 422 Unprocessable Entity


def test_update_post_that_doesnt_exist(authorized_client):
    data = {
        'title': 'updated title',
        'content': 'updated content'
    }
    response = authorized_client.put('/posts/100', json=data)
    assert response.status_code == 404
