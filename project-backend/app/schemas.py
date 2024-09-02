from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional
from datetime import datetime


# Token model schema for authentication
class Token(BaseModel):
    """
    Schema to represent an authentication token.
    """
    access_token: str
    token_type: str

# Schema to represent token data
class TokenData(BaseModel):
    """
    Schema to store token-related data.
    """
    id: Optional[int] = None

# Base schema for user model
class UserBase(BaseModel):
    """
    Base schema for user data.
    """
    # username: str  # Commented out username field
    email: EmailStr

# Schema for creating a new user
class UserCreate(UserBase):
    """
    Schema for creating a new user. Inherits from UserBase.
    """
    password: str 
    # constr(min_length=6)  # Commented constraint on password length

# Schema for updating user information
class UserUpdate(UserBase):
    """
    Schema for updating user information. Inherits from UserBase.
    """
    profile_picture: Optional[str] = None
    bio: Optional[str] = None

# Schema for returning user information
class UserResponse(UserBase):
    """
    Schema for returning user information in responses. Inherits from UserBase.
    """
    id: int
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True  # Enables ORM mode for compatibility with SQLAlchemy models

# Schema for returning limited user information (username and email)
class UserNameResponse(BaseModel):
    """
    Schema to return a simplified user response, specifically for the username and email.
    """
    email: EmailStr

# Schema for changing a user's password
class ChangePassword(BaseModel):
    """
    Schema for changing the user's password.
    """
    old_password: str
    new_password: str

# Base schema for tags
class TagBase(BaseModel):
    """
    Base schema for tags associated with blog posts.
    """
    name: str

# Schema for creating a tag
class TagCreate(TagBase):
    """
    Schema for creating a new tag. Inherits from TagBase.
    """
    pass

# Schema for returning tag information
class TagResponse(TagBase):
    """
    Schema for returning tag information. Inherits from TagBase.
    """
    id: int

    class Config:
        orm_mode = True

# Base schema for comments
class CommentBase(BaseModel):
    """
    Base schema for comments made on blog posts.
    """
    content: str

# Schema for creating a comment
class CommentCreate(CommentBase):
    """
    Schema for creating a new comment. Inherits from CommentBase.
    """
    # post_id: int  # Commented out post_id field
    pass

# Schema for returning comment information
class CommentResponse(CommentBase):
    """
    Schema for returning comment information. Inherits from CommentBase.
    """
    id: int
    created_at: datetime
    author: UserResponse

    class Config:
        orm_mode = True

# Base schema for blog posts
class BlogPostBase(BaseModel):
    """
    Base schema for blog posts.
    """
    title: str 
    # constr(min_length=1, max_length=255)  # Commented constraint for title length
    content: str

# Schema for creating a blog post
class BlogPostCreate(BlogPostBase):
    """
    Schema for creating a new blog post. Inherits from BlogPostBase.
    """
    # slug: str  # Commented out slug field
    tags: Optional[List[str]] = []

# Schema for updating a blog post
class BlogPostUpdate(BlogPostBase):
    """
    Schema for updating an existing blog post. Inherits from BlogPostBase.
    """
    is_published: Optional[bool] = False
    category_id: Optional[int] = None
    tags: Optional[List[str]] = []

# Schema for returning blog post information
class BlogPostResponse(BlogPostBase):
    """
    Schema for returning detailed blog post information. Inherits from BlogPostBase.
    """
    id: int
    title: str
    slug: str
    published_at: Optional[datetime] = None
    is_published: bool
    category: Optional[str] = None
    tags: List[TagResponse]
    comments: List[CommentResponse]
    author: UserNameResponse

    class Config:
        orm_mode = True

# Base schema for categories
class CategoryBase(BaseModel):
    """
    Base schema for blog post categories.
    """
    name: str

# Schema for creating a category
class CategoryCreate(CategoryBase):
    """
    Schema for creating a new category. Inherits from CategoryBase.
    """
    description: Optional[str] = None

# Schema for returning category information
class CategoryResponse(CategoryBase):
    """
    Schema for returning category information. Inherits from CategoryBase.
    """
    id: int
    description: Optional[str] = None

    class Config:
        orm_mode = True

# Base schema for likes
class LikeBase(BaseModel):
    """
    Base schema for likes on blog posts.
    """
    post_id: int

# Schema for creating a like
class LikeCreate(LikeBase):
    """
    Schema for creating a new like. Inherits from LikeBase.
    """
    pass

# Schema for returning like information
class LikeResponse(LikeBase):
    """
    Schema for returning like information. Inherits from LikeBase.
    """
    id: int
    user: UserResponse

    class Config:
        orm_mode = True

# Base schema for notifications
class NotificationBase(BaseModel):
    """
    Base schema for notifications sent to users.
    """
    message: str
    is_read: bool = False

# Schema for creating a notification
class NotificationCreate(NotificationBase):
    """
    Schema for creating a new notification. Inherits from NotificationBase.
    """
    user_id: int
    post_id: int

# Schema for returning notification information
class NotificationResponse(NotificationBase):
    """
    Schema for returning notification information. Inherits from NotificationBase.
    """
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
