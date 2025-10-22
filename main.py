from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from app.routers import auth, dashboard

# Crear aplicación FastAPI
app = FastAPI(
    title="FastAPI Authentication Backend",
    description="Backend de autenticación y gestión de usuarios para el dashboard del sistema",
    version="1.0.0"
)


# Configurar CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])

@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {"status": "healthy", "service": "fastapi_auth"}

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {"message": "FastAPI Authentication Backend", "status": "running"}

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    import uvicorn
    uvicorn.run(app, host=host, port=port)