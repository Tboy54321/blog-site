from app import schemas
import pytest

def test_get_all_blogs(authorized_client, test_posts):
    response = authorized_client.get("/posts/")

    def validate(post):
        return schemas.BlogPostResponse(**post)
    post_map = map(validate, response.json())
    posts = list(post_map)
    
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

def test_unauthenticated_get_all_blogs(client, test_posts):
    response = client.get("/posts/")

    assert response.status_code == 401

def test_get_all_empty_blogs(authorized_client):
    response = authorized_client.get("/posts/")

    assert response.status_code == 200


def test_get_all_my_blogs(authorized_client, test_posts, test_user):
    response = authorized_client.get("/myposts/")
    posts = response.json()

    for post in posts:
        assert post['author']['email'] == test_user['email']

    assert response.status_code == 200

def test_unauthenticated_get_all_my_blogs(client, test_posts):
    response = client.get("/myposts/")
    
    assert response.status_code == 401

def test_get_all_user_blogs(authorized_client, test_posts, test_user):
    response = authorized_client.get(f"/allposts/{test_user['email']}/")

    assert response.status_code == 200

def test_unauthenticated_get_all_user_blogs(client, test_posts, test_user):
    response = client.get(f"/allposts/{test_user['email']}/")

    assert response.status_code == 401

def test_get_one_post(authorized_client, test_posts, test_user):
    response = authorized_client.get(f"/one-post/{test_posts[0].id}/")
    print(response.json())

    assert response.status_code == 200

def test_unauthenticated_get_one_post(client, test_posts, test_user):
    response = client.get(f"/one-post/{test_user['id']}/")

    assert response.status_code == 401

def test_create_post(authorized_client, test_user):
    response = authorized_client.post("/createpost/", json={"title": "A whole new title", "content": "Good contents to the new title"})
    new_post = schemas.BlogPostResponse(**response.json())

    assert new_post.title == "A whole new title"
    assert response.status_code == 200

@pytest.mark.parametrize("title, content, status_code", [
    ("Another new title", None, 422),
    (None, "Another content to an empty title", 422),
    (None, None, 422)
])
def test_failed_create_post(authorized_client, test_user, title, content, status_code):
    response = authorized_client.post("/createpost/", json={"title": title, "content": content})

    assert response.status_code == status_code

def test_unauthenticated_create_post(client, test_user):
    response = client.post("/createpost/", json={"title": "A whole new title", "content": "Good contents to the new title"})

    assert response.status_code == 401

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "all title",
        "content": "1st content",
        "slug": "1st-title"
    }
    response = authorized_client.put(f"/updatepost/{test_posts[0].id}", json = data)

    assert response.status_code == 200

@pytest.mark.parametrize("title, content, slug, status_code", [
    ("Another new title", None, "Another-new-title" ,422),
    (None, "Another content to an empty title", None, 422),
    (None, None, None , 422)
])
def test_failed_update_post(authorized_client, test_posts, title, content, slug, status_code):
    data = {
        "title": title,
        "content": content,
        "slug": slug
    }
    response = authorized_client.put(f"/updatepost/{test_posts[0].id}", json = data)

    assert response.status_code == status_code

def test_unauthenticated_update_post(client, test_posts):
    data = {
        "title": "all title",
        "content": "1st content",
        "slug": "1st-title"
    }
    response = client.put(f"/updatepost/{test_posts[0].id}/", json = data)
    assert response.status_code == 401
    assert response.json()['detail'] == "Not authenticated"

def test_unauthorized_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "all title",
        "content": "1st content",
        "slug": "1st-title"
    }
    response = authorized_client.put(f"/updatepost/{test_posts[3].id}/", json = data)

    assert response.status_code == 401
    assert response.json()['detail'] == "Not Authorized"

def test_wrong_post_id_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "all title",
        "content": "1st content",
        "slug": "1st-title"
    }
    wrong_id = 800
    response = authorized_client.put(f"/updatepost/{wrong_id}", json = data)

    assert response.status_code == 404
    assert response.json()['detail'] == f"Post with id: {wrong_id} was not found"

def test_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/deletepost/{test_posts[0].id}/")

    response.status_code == 200

def test_unauthorized_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/deletepost/{test_posts[3].id}/")

    assert response.status_code == 401
    assert response.json()['detail'] == "Not Authorized"

def test_unauthenticated_delete_post(client, test_user, test_posts):
    response = client.delete(f"/deletepost/{test_posts[0].id}/")

    response.status_code == 401
    assert response.json()['detail'] == "Not authenticated"
