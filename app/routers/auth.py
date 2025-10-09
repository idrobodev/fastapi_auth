from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from ..models.user import User, UserUpdate, Token, UserRole, UserLogin, UserCreate
from ..models.database import db, verify_password
from ..utils.auth import (
    create_access_token,
    get_current_active_user,
    check_permission
)
from typing import Dict

class RegisterRequest(BaseModel):
    email: str
    password: str
    role: str

router = APIRouter()

@router.post("/register")
async def register(request: RegisterRequest):
    """Registrar un nuevo usuario"""
    try:
        user_role = UserRole(request.role)
        user_create = UserCreate(email=request.email, password=request.password, role=user_role)
        db.create_user(user_create)
        return {"message": "User registered successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(credentials: UserLogin):
    """Iniciar sesión y obtener token de acceso"""
    user = db.get_user_by_email(credentials.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear token de acceso
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value}
    )

    # Convertir user a dict para la respuesta
    user_data = {
        "id": user.id,
        "email": user.email,
        "role": user.role.value,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat()
    }

    return {
        "data": {
            "user": user_data,
            "token": access_token
        },
        "error": None
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """Cerrar sesión (simulado - en una implementación real se invalidaría el token)"""
    return {"message": "Sesión cerrada exitosamente"}

@router.post("/reset-password")
async def reset_password(email: str):
    """Restablecer contraseña (simulado - en producción enviaría email)"""
    user = db.get_user_by_email(email)
    if not user:
        # Por seguridad, no revelamos si el email existe o no
        return {"message": "Si el email existe, se ha enviado un enlace de restablecimiento"}

    # En una implementación real, aquí se generaría un token temporal
    # y se enviaría por email
    return {"message": "Si el email existe, se ha enviado un enlace de restablecimiento"}

@router.put("/profile")
async def update_profile(
    profile_data: UserUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Actualizar perfil del usuario actual"""
    try:
        updated_user = db.update_user(current_user.id, profile_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return {
            "data": updated_user,
            "error": None
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/permission")
async def check_user_permission(
    role: str,
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, bool]:
    """Verificar si el usuario tiene el permiso requerido"""
    try:
        required_role = UserRole(role)
        has_permission = check_permission(required_role, current_user)
        return {"hasPermission": has_permission}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rol inválido"
        )