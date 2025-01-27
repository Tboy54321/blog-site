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
