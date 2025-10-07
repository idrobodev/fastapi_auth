from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, dashboard
from app.models.database import engine
from app.models import user

# Create database tables (with error handling)
try:
    user.Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Warning: Could not connect to database: {e}")
    print("Application will start without database initialization")
    print("Make sure DATABASE_URL environment variable is set correctly")

app = FastAPI(title="FastAPI Auth", description="Authentication API for React project", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Adjust for your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/")
async def root():
    return {"message": "FastAPI Auth API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)