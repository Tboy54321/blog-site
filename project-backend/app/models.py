from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Table
from sqlalchemy.orm import relationship
from database import Base
# from .database import Base
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

post_tag_association = Table(
    'post_tag',
    Base.metadata,
    Column('post_id', ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

# User Model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    # username = Column(String(150), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    profile_picture = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    posts = relationship('BlogPost', back_populates='author')
    comments = relationship('Comment', back_populates='author')
    likes = relationship('Like', back_populates='user', cascade="all, delete")
    notifications = relationship('Notification', back_populates='user', cascade="all, delete")

# BlogPost Model
class BlogPost(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    published_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)

    author = relationship('User', back_populates='posts')
    category = relationship('Category', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    tags = relationship('Tag', secondary=post_tag_association, back_populates='posts')
    likes = relationship('Like', back_populates='post', cascade="all, delete")
    notifications = relationship('Notification', back_populates='post', cascade="all, delete")

# Category Model
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    posts = relationship('BlogPost', back_populates='category')

# Tag Model
class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    posts = relationship('BlogPost', secondary=post_tag_association, back_populates='tags')

# Comment Model
class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

    author = relationship('User', back_populates='comments')
    post = relationship('BlogPost', back_populates='comments')

# Like Model (Optional)
class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, primary_key=True)

    user = relationship('User', back_populates='likes')
    post = relationship('BlogPost', back_populates='likes')


class TokenBlacklist(Base):
    __tablename__ = 'token_blacklist'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, index=True, unique=True)
    blacklisted_on = Column(DateTime, default=datetime.utcnow)


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")
    post = relationship("BlogPost", back_populates="notifications")