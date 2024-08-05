from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


# Base schema
class UserBase(BaseModel):
    # username: str
    email: EmailStr

# Schema for creating a new user
class UserCreate(UserBase):
    password: str 
    # constr(min_length=6)

# Schema for updating user information
class UserUpdate(UserBase):
    profile_picture: Optional[str] = None
    bio: Optional[str] = None

# Schema for returning user information
class UserResponse(UserBase):
    id: int
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True




class BlogPostBase(BaseModel):
    title: str 
    # constr(min_length=1, max_length=255)
    content: str

# Schema for creating a blog post
class BlogPostCreate(BlogPostBase):
    tags: Optional[List[str]] = []

# Schema for updating a blog post
class BlogPostUpdate(BlogPostBase):
    is_published: Optional[bool] = False
    category_id: Optional[int] = None
    tags: Optional[List[str]] = []


# Schema for returning blog post information
class BlogPostResponse(BlogPostBase):
    id: int
    slug: str
    published_at: Optional[datetime] = None
    is_published: bool
    author: UserResponse
    category: Optional[str] = None
    tags: List[str] = []
    comments: List[str] = []

    class Config:
        orm_mode = True




class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    description: Optional[str] = None

    class Config:
        orm_mode = True




class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int

    class Config:
        orm_mode = True



class CommentBase(BaseModel):
    content: str

# Schema for creating a comment
class CommentCreate(CommentBase):
    post_id: int

# Schema for returning comment information
class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    author: UserResponse

    class Config:
        orm_mode = True



class LikeBase(BaseModel):
    post_id: int

class LikeCreate(LikeBase):
    pass

class LikeResponse(LikeBase):
    id: int
    user: UserResponse

    class Config:
        orm_mode = True
