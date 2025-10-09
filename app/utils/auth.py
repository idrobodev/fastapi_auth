from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..models.user import User, TokenData, UserRole
from ..models.database import db
import os

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production-make-it-very-long-and-random")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crear token de acceso JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """Verificar y decodificar token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None:
            raise JWTError("Token inválido")
        token_data = TokenData(email=email, role=role)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Obtener usuario actual desde token"""
    token_data = verify_token(credentials.credentials)
    user = db.get_user_by_email(token_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(
        id=user.id,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Obtener usuario activo actual"""
    return current_user

def require_role(required_role: UserRole):
    """Dependencia para requerir un rol específico"""
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere rol {required_role}"
            )
        return current_user
    return role_checker

def require_admin(current_user: User = Depends(get_current_active_user)):
    """Dependencia para requerir rol administrador"""
    return require_role(UserRole.ADMINISTRADOR)(current_user)

def check_permission(required_role: UserRole, current_user: User = Depends(get_current_active_user)) -> bool:
    """Verificar si el usuario tiene el rol requerido"""
    role_hierarchy = {
        UserRole.ADMINISTRADOR: 2,
        UserRole.CONSULTA: 1
    }

    user_level = role_hierarchy.get(current_user.role, 0)
    required_level = role_hierarchy.get(required_role, 0)

    return user_level >= required_level