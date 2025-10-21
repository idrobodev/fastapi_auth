from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import yaml

# Cargar variables de entorno
load_dotenv()

from app.routers import auth, dashboard

# Crear aplicación FastAPI
app = FastAPI(
    title="FastAPI Authentication Backend",
    description="Backend de autenticación y gestión de usuarios para el dashboard del sistema",
    version="1.0.0"
)

# Cargar esquema OpenAPI desde archivo YAML
with open("openapi.yaml", "r") as f:
    openapi_schema = yaml.safe_load(f)
app.openapi_schema = openapi_schema

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
app.include_router(auth.router, prefix="", tags=["authentication"])
app.include_router(dashboard.router, prefix="", tags=["dashboard"])

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