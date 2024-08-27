from app import schemas

def test_get_all_blogs(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    print(response.json())

    def validate(post):
        return schemas.BlogPostResponse(**post)
    
    post_map = map(validate, response.json())
    posts = list(post_map)
    print(posts)
    
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200