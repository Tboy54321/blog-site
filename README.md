<h1 align="center">Blog API with User Interaction and Notifications</h1>

This project provides a Blog API where users can create, update, like, and comment on blog posts. It includes user management features such as sign-up, login, profile update, password change, and account deletion. Additionally, the project has notification functionality to alert users about events like when their posts are liked.

## Features

### User Registration and Authentication
- Sign up new users
- User login with JWT-based authentication
- User profile management (update information, change password)
- Password reset functionality
- Account deletion

### Blog Management
- Create blog posts
- Edit or delete posts
- Like and unlike posts
- View all posts or specific posts by author

### Notifications
- Receive notifications when a user likes a post

### Database and Schema Migrations
- Schema migrations handled with Alembic for database management

## Technologies Used
- **FastAPI** for building the API.
- **SQLAlchemy** for ORM-based database interaction.
- **Alembic** for handling database migrations.
- **Pydantic** for data validation.
- **OAuth2 with JWT** for secure authentication.
- **PostgreSQL** for database storage.
- **Postman** for testing and documenting API endpoints.

## Setup Instructions

1. **Clone the Repository**  
   First, clone the repository to your local machine:
   ```bash
   git clone <your-repository-url>

2. Navigate to the Project Folder
   After cloning, navigate to the project directory:
   ```bash
   cd <your-project-folder>

3. Install Dependencies
   Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt

4. Setup the Database
   Run the migrations to set up the database:
   ```bash
   alembic upgrade head

5. Start the Application
   Finally, run the application:
   ```bash
   uvicorn app.main:app --reload

6. Accessing the API
   By default, the app will be running on http://127.0.0.1:8000. You can access the OpenAPI documentation at http://127.0.0.1:8000/docs for easy API exploration.

## Endpoints

### User Authentication
- POST /signup/: Register a new user (requires email and password).
- POST /login/: User login, returns JWT token.

### User Profile
- GET /profile/: Retrieve current user profile.
- PUT /update/: Update current user profile information.
- PUT /change-password/: Change the password of the current user.
- DELETE /delete-account/: Delete the user's account.

### Blog Post Management
- POST /posts/{id}/like: Like a specific post (requires authentication).
- DELETE /posts/{id}/unlike: Unlike a specific post.
- GET /posts/: Retrieve all blog posts.
- GET /posts/{id}/: Retrieve a specific post by ID.

### Notifications
- GET /notifications/: Retrieve all notifications for the current user.

## Database Models

### User
- id: Primary key
- email: Unique email address
- password: Hashed password
- created_at: Timestamp when the user was created
### BlogPost
- id: Primary key
- author_id: Foreign key to User
- title: Title of the blog post
- content: Content of the blog post
- created_at: Timestamp when the post was created
### Like
- user_id: Foreign key to User
- post_id: Foreign key to BlogPost
### Notification
- user_id: Foreign key to User (recipient of the notification)
- post_id: Foreign key to BlogPost (the post related to the notification)
- message: Notification message
- timestamp: Timestamp of the notification

## Migrations
Alembic is set up to handle schema migrations for the database.
1. To create a new migration after making changes to models:
   ```bash
   alembic revision --autogenerate -m "message describing changes"
2. To apply the migrations:
   ```bash
   alembic upgrade head

## Testing

## Acknowledgements
FastAPI Documentation: https://fastapi.tiangolo.com/
SQLAlchemy Documentation: https://www.sqlalchemy.org/
