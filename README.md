# FastAPI Auth

A FastAPI project for user authentication, designed to serve login functionality for a React application. It connects to a PostgreSQL database.

## Features

- User registration and login
- JWT-based authentication
- Protected routes
- PostgreSQL database integration

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. The database connection is configured to connect to the provided PostgreSQL instance.

3. Run the application:
   ```
   uvicorn main:app --reload
   ```

4. The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /auth/register` - Register a new user
- `POST /auth/token` - Login and get access token
- `GET /auth/me` - Get current user info (requires authentication)
- `GET /dashboard/protected` - Protected route example

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection URL (optional, defaults to provided URL)

## Security Note

Change the `SECRET_KEY` in `app/utils/auth.py` for production use.