from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
# import models, schemas, oauth2 [UVICORN]
import app.models as models, app.schemas as schemas, app.oauth2 as oauth2
from sqlalchemy.orm import Session
# from database import get_db [UVICRON]
from app.database import get_db
import re
from typing import List

router = APIRouter(
    tags=["Blogs Page"]
)


def generate_slugs(title: str):
    """
    Function to generate URL-friendly slugs from blog post titles.
    Replaces spaces with hyphens and removes special characters.
    """
    slug = title.lower()
    slug = slug.replace(" ", "-")
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug


@router.get("/posts/", response_model=List[schemas.BlogPostResponse], status_code=status.HTTP_200_OK)
def get_all_blogs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Endpoint to retrieve all blog posts.
    """
    all_blogs = db.query(models.BlogPost).all()
    return all_blogs


@router.get("/posts/", response_model=List[schemas.BlogPostResponse])
def search_blogs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: str = ""):
    """
    Endpoint to search blog posts by title.
    """
    all_blogs = db.query(models.BlogPost).filter(models.BlogPost.title.contains(search)).all()
    return all_blogs


@router.get("/myposts/", response_model=List[schemas.BlogPostResponse])
def get_all_my_blogs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Endpoint to retrieve all blog posts by the current user.
    """
    all_my_blogs = db.query(models.BlogPost).filter(models.BlogPost.author_id == current_user.id).all()
    return all_my_blogs


@router.get("/allposts/{email}/", response_model=List[schemas.BlogPostResponse])
def get_all_user_blogs(email: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Endpoint to retrieve all blog posts by a specific user based on their email.
    """
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    all_my_blogs = db.query(models.BlogPost).filter(models.BlogPost.author_id == user.id).all()
    
    return all_my_blogs


@router.get("/posts/{email}/", response_model=List[schemas.BlogPostResponse])
def get_all_user_blogs_by_filter(email: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 5):
    """
    Endpoint to retrieve all blog posts by a specific user with a limit on the number of posts returned.
    """
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    all_my_blogs = db.query(models.BlogPost).filter(models.BlogPost.author_id == user.id).limit(limit).all()
    
    return all_my_blogs


@router.get("/one-post/{id}/", response_model=schemas.BlogPostResponse)
def get_one_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Endpoint to retrieve a single blog post by its ID.
    """
    blog = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")

    return blog


# NOT YET WORKING
@router.get("/getpost/{tag_name}/", response_model=List[schemas.BlogPostResponse])
def get_post_by_category(tag_name: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Endpoint to retrieve blog posts by a specific tag. Currently not working.
    """
    posts = db.query(models.BlogPost).join(models.BlogPost.tags).filter(models.Tag.name == tag_name).all()
    print(posts)

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts found with tag: {tag_name}")
    
    return posts


@router.post("/createpost/", response_model=schemas.BlogPostResponse)
def create_post(blog_post: schemas.BlogPostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Endpoint to create a new blog post.
    """
    # HANDLE THIS ERROR: if not blog_post.title or not blog_post.content:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Title and content cannot be empty."
    #     )
    # Handle this error : DETAIL:  Key (slug)=(undrstading-the-baics-f-rest-apis) already exists. repeated SLUG
    # HANDLING SLUG UNIQUENESS
    slug = generate_slugs(blog_post.title)
    no_of_characters = sum(len(char) for char in blog_post.title)
    
    if no_of_characters >= 50:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title should not be more than 50 characters")

    new_post = models.BlogPost(
        title=blog_post.title,
        content=blog_post.content,
        author_id=current_user.id,
        slug = slug
    )

    tags = []
    for tag_name in blog_post.tags:
        tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        if not tag:
            tag = models.Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tags.append(tag)

    new_post.tags = tags

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/updatepost/{id}/", response_model=schemas.BlogPostResponse)
def update_post(updated_post: schemas.BlogPostUpdate, id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Endpoint to update an existing blog post by its ID.
    """
    post_query = db.query(models.BlogPost).filter(models.BlogPost.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    update_data = updated_post.dict(exclude_unset=True)

    if 'tags' in update_data:
        post.tags = []

        new_tags = []
        for tag_name in update_data['tags']:
            tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            new_tags.append(tag)

        post.tags = new_tags
        del update_data["tags"]

    post_query.update(update_data, synchronize_session=False)
    # Handle the tags update
    
    db.commit()
    print(post.tags)
    return post


@router.delete("/deletepost/{id}/", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    """
    Endpoint to delete a blog post by its ID.
    """
    delete_query = db.query(models.BlogPost).filter(models.BlogPost.id == id)
    deleted_post = delete_query.first()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    if deleted_post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    

    # delete_associations = db.query(models.post_tag_association).filter(models.post_tag_association.c.post_id == id)
    # delete_associations.delete(synchronize_session=False)

    delete_query.delete(synchronize_session=False)
    db.commit()
    return (deleted_post)


# Endpoint to handle searching of posts based on title