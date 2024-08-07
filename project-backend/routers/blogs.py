from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
import models, schemas, oauth2
from sqlalchemy.orm import Session
from database import get_db
import re

router = APIRouter(tags=["Blogs Page"])


def generate_slugs(title: str):
    slug = title.lower()
    slug = slug.replace(" ", "-")
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug


@router.get("/posts")
def get_all_blogs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    all_blogs = db.query(models.BlogPost).all()
    return all_blogs


@router.get("/posts/{id}")
def get_one_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    blog = db.query(models.BlogPost).filter(models.BlogPost.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    
    return blog


@router.get("/getpost/{tag_name}")
def get_post_by_category(tag_name: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    posts = db.query(models.BlogPost).join(models.BlogPost.tags).filter(models.Tag.name == tag_name).all()
    print(posts)

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No posts found with tag: {tag_name}")
    
    return posts


@router.post("/createpost")
def create_post(blog_post: schemas.BlogPostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # HABDLE THIS ERROR: if not blog_post.title or not blog_post.content:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Title and content cannot be empty."
    #     )
    # Handle this error : DETAIL:  Key (slug)=(undrstading-the-baics-f-rest-apis) already exists. repeated SLUG
    slug = generate_slugs(blog_post.title)
    new_post = models.BlogPost(
        **blog_post.dict(),
        author_id=current_user.id,
        slug = slug
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"blog post": new_post}


@router.put("/updatepost/{id}")
def update_post(updated_post: schemas.BlogPostUpdate, id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    old_post = db.query(models.BlogPost).filter(models.BlogPost.id == id)
    post = old_post.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    update_data = updated_post.dict(exclude_unset=True)
    tags = update_data.pop('tags', None)  # Remove tags from the dict if present
    old_post.update(update_data, synchronize_session=False)
    # Handle the tags update
    # HANDLING AND LINKING TAGS TO THE BLOG POST
    
    db.commit()

    return {"Updated Post": old_post.first()}


@router.delete("/deletepost/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    delete_query = db.query(models.BlogPost).filter(models.BlogPost.id == id)
    deleted_post = delete_query.first()

    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    if not deleted_post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    delete_query.delete(synchronize_session=False)
    db.commit()
    return (deleted_post)