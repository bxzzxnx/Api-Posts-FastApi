def test_get_all_votes(client):
    response = client.get('/vote')
    assert response.status_code == 200


def test_unauthorized_post_vote(client):
    data = {
        'post_id': 1,
        'vote_dir': 1
    }
    response = client.post('/vote', json=data)
    assert response.status_code == 401


def test_vote_on_post(authorized_client, test_posts):
    data = {
        'post_id': test_posts[0].id,
        'vote_dir': 1
    }
    response = authorized_client.post('/vote', json=data)
    assert response.status_code == 201
    assert response.json().get('message') == 'Successfully voted'


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    data = {
        'post_id': test_posts[0].id,
        'vote_dir': 1
    }
    response = authorized_client.post('/vote', json=data)
    assert response.status_code == 409  # Conflict


def test_delete_vote(authorized_client, test_vote, test_posts):
    data = {
        'post_id': test_posts[0].id,
        'vote_dir': 0
    }

    response = authorized_client.post('/vote', json=data)
    assert response.json().get('message') == 'Voto deletado'
    assert response.status_code == 201


def test_delete_vote_doesnt_exist(authorized_client, test_vote):
    data = {
        'post_id': 999,
        'vote_dir': 1
    }

    response = authorized_client.post('/vote', json=data)
    assert response.status_code == 404
    assert response.json().get('detail') == 'Post not found'


def test_vote_unauthorized_user(client, test_vote, test_posts):
    data = {
        'post_id': test_posts[0].id,
        'vote_dir': 1
    }

    response = client.post('/vote', json=data)
    assert response.status_code == 401
