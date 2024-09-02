from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Table
from sqlalchemy.orm import relationship
# from database import Base [UVICORN]
from app.database import Base
from datetime import datetime


# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(150), unique=True, nullable=False, index=True)
#     email = Column(String(150), unique=True, nullable=False, index=True)
#     password = Column(String, nullable=False)
#     profile_picture = Column(String, nullable=True)
#     bio = Column(Text, nullable=True)
#     is_active = Column(Boolean, default=True)
#     is_admin = Column(Boolean, default=False)

#     posts = relationship('BlogPost', back_populates='author')
#     comments = relationship('Comment', back_populates='author')
#     likes = relationship('Like', back_populates='user')



# # class Users(Base):

# #     __tablename__ = "users"
# #     id = Column(Integer, primary_key=True, nullable=False)
# #     email = Column(String, nullable=False, unique=True)
# #     password = Column(String, nullable=False)

# Association table for many-to-many relationship between BlogPost and Tag models
post_tag_association = Table(
    'post_tag',
    Base.metadata,
    Column('post_id', ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

# User Model to represent users in the application
class User(Base):
    """
    User model that represents a user of the system. 
    A user can have multiple posts, comments, likes, and notifications.
    """ 
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    # username = Column(String(150), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # Relationships with other models
    posts = relationship('BlogPost', back_populates='author')
    comments = relationship('Comment', back_populates='author')
    likes = relationship('Like', back_populates='user', cascade="all, delete")
    notifications = relationship('Notification', back_populates='user', cascade="all, delete")

# BlogPost Model to represent blog posts in the application
class BlogPost(Base):
    """
    BlogPost model that represents a blog post created by a user. 
    A post can belong to a category, have multiple tags, comments, likes, and notifications.
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    published_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)

    # Relationships with other models
    author = relationship('User', back_populates='posts')
    category = relationship('Category', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    tags = relationship('Tag', secondary=post_tag_association, back_populates='posts')
    likes = relationship('Like', back_populates='post', cascade="all, delete")
    notifications = relationship('Notification', back_populates='post', cascade="all, delete")

# Category Model to represent post categories
class Category(Base):
    """
    Category model that represents a category a blog post can belong to.
    """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relationship with BlogPost model
    posts = relationship('BlogPost', back_populates='category')

# Tag Model to represent post tags
class Tag(Base):
    """
    Tag model that represents a tag associated with blog posts.
    """
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    # Relationship with BlogPost model (many-to-many)
    posts = relationship('BlogPost', secondary=post_tag_association, back_populates='tags')

# Comment Model to represent post comments
class Comment(Base):
    """
    Comment model that represents a comment made by a user on a blog post.
    """
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

    # Relationships with User and BlogPost models
    author = relationship('User', back_populates='comments')
    post = relationship('BlogPost', back_populates='comments')

# Like Model to represent post likes
class Like(Base):
    """
    Like model that represents a like given by a user to a blog post.
    """
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, primary_key=True)

    # Relationships with User and BlogPost models
    user = relationship('User', back_populates='likes')
    post = relationship('BlogPost', back_populates='likes')


# TokenBlacklist Model to store blacklisted tokens (for logout)
class TokenBlacklist(Base):
    """
    TokenBlacklist model to store blacklisted tokens after logout to prevent reuse.
    """
    __tablename__ = 'token_blacklist'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True, unique=True)
    blacklisted_on = Column(DateTime, default=datetime.utcnow)



class RefreshToken(Base):
    """
    RefreshToken model to store refresh tokens and their expiration times.
    """
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)


# Notification Model to represent notifications for users
class Notification(Base):
    """
    Notification model that represents notifications sent to users.
    """
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships with User and BlogPost models
    user = relationship("User", back_populates="notifications")
    post = relationship("BlogPost", back_populates="notifications")