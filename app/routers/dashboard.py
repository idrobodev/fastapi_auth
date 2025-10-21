from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict
from ..models.user import User, UserCreate, UserUpdate
from ..models.database import db
from ..utils.auth import get_current_active_user, require_admin
from ..models.user import UserRole

router = APIRouter()

@router.get("/usuarios", response_model=List[User])
async def get_usuarios(current_user: User = Depends(require_admin)):
    """Obtener lista de todos los usuarios (solo administradores)"""
    try:
        users = db.get_all_users()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}"
        )

@router.post("/usuarios")
async def create_usuario(
    user_data: UserCreate,
    current_user: User = Depends(require_admin)
):
    """Crear nuevo usuario (solo administradores)"""
    try:
        new_user = db.create_user(user_data)
        return {
            "data": new_user,
            "error": None
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}"
        )

@router.put("/usuarios/{user_id}")
async def update_usuario(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(require_admin)
):
    """Actualizar usuario existente (solo administradores)"""
    try:
        updated_user = db.update_user(user_id, user_data)
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar usuario: {str(e)}"
        )

@router.delete("/usuarios/{user_id}")
async def delete_usuario(
    user_id: int,
    current_user: User = Depends(require_admin)
):
    """Eliminar usuario (solo administradores)"""
    try:
        # No permitir eliminar al propio usuario
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes eliminar tu propio usuario"
            )

        success = db.delete_user(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        return {
            "error": None,
            "message": "Usuario eliminado exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar usuario: {str(e)}"
        )

@router.get("/dashboard/stats")
async def get_dashboard_stats(current_user: User = Depends(get_current_active_user)):
    """Obtener estadísticas del dashboard"""
    try:
        users = db.get_all_users()
        total_users = len(users)
        admin_count = len([u for u in users if u.role == UserRole.ADMINISTRADOR])
        consulta_count = len([u for u in users if u.role == UserRole.CONSULTA])

        return {
            "participantes": total_users,  # Simulado para compatibilidad
            "mensualidades": 0,  # Simulado para compatibilidad
            "total_users": total_users,
            "admin_users": admin_count,
            "consulta_users": consulta_count
        }
    except Exception as e:
        return {
            "participantes": 0,
            "mensualidades": 0,
            "error": str(e)
        }