from sqlalchemy import create_engine, Column, Integer, String, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
from datetime import datetime
from .user import User, UserCreate, UserUpdate, UserRole
import hashlib
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de hash de contraseñas
def hash_password(password: str) -> str:
    """Hash de contraseña usando SHA-256 con salt"""
    salt = os.getenv("PASSWORD_SALT", "default_salt").encode()
    return hashlib.sha256(salt + password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    salt = os.getenv("PASSWORD_SALT", "default_salt").encode()
    return hashlib.sha256(salt + plain_password.encode()).hexdigest() == hashed_password

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/auth_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class UserModel(Base):
    """Modelo SQLAlchemy para User"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CONSULTA)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Crear las tablas
Base.metadata.create_all(bind=engine)

class DatabaseService:
    """Servicio de base de datos usando SQLAlchemy"""

    def __init__(self):
        self.initialize_default_users()

    def get_db(self) -> Session:
        """Obtener sesión de base de datos"""
        return SessionLocal()

    def create_user(self, user: UserCreate) -> User:
        """Crear nuevo usuario"""
        db = self.get_db()
        try:
            # Verificar si el email ya existe
            existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
            if existing_user:
                raise ValueError("Email already registered")

            # Crear nuevo usuario
            now = datetime.utcnow()
            db_user = UserModel(
                email=user.email,
                password_hash=hash_password(user.password),
                role=user.role,
                created_at=now,
                updated_at=now
            )

            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            return User(
                id=db_user.id,
                email=db_user.email,
                role=db_user.role,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
        finally:
            db.close()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        db = self.get_db()
        try:
            db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if db_user:
                return User(
                    id=db_user.id,
                    email=db_user.email,
                    role=db_user.role,
                    created_at=db_user.created_at,
                    updated_at=db_user.updated_at
                )
            return None
        finally:
            db.close()

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """Obtener usuario por email (con hash de contraseña)"""
        db = self.get_db()
        try:
            return db.query(UserModel).filter(UserModel.email == email).first()
        finally:
            db.close()

    def get_all_users(self) -> list[User]:
        """Obtener todos los usuarios"""
        db = self.get_db()
        try:
            db_users = db.query(UserModel).all()
            return [
                User(
                    id=user.id,
                    email=user.email,
                    role=user.role,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                )
                for user in db_users
            ]
        finally:
            db.close()

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Actualizar usuario"""
        db = self.get_db()
        try:
            db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if not db_user:
                return None

            # Verificar email único si se está cambiando
            if user_update.email and user_update.email != db_user.email:
                existing_user = db.query(UserModel).filter(
                    UserModel.email == user_update.email,
                    UserModel.id != user_id
                ).first()
                if existing_user:
                    raise ValueError("Email already registered")

            # Actualizar campos
            if user_update.email:
                db_user.email = user_update.email
            if user_update.password:
                db_user.password_hash = hash_password(user_update.password)
            if user_update.role:
                db_user.role = user_update.role

            db_user.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_user)

            return User(
                id=db_user.id,
                email=db_user.email,
                role=db_user.role,
                created_at=db_user.created_at,
                updated_at=db_user.updated_at
            )
        finally:
            db.close()

    def delete_user(self, user_id: int) -> bool:
        """Eliminar usuario"""
        db = self.get_db()
        try:
            db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
            if db_user:
                db.delete(db_user)
                db.commit()
                return True
            return False
        finally:
            db.close()

    def initialize_default_users(self):
        """Inicializar usuarios por defecto"""
        db = self.get_db()
        try:
            # Verificar si ya existen usuarios
            existing_count = db.query(UserModel).count()
            if existing_count > 0:
                return

            # Crear usuarios por defecto
            default_users = [
                {
                    "email": "admin@example.com",
                    "password": "admin123",
                    "role": UserRole.ADMINISTRADOR
                },
                {
                    "email": "consulta@example.com",
                    "password": "consulta123",
                    "role": UserRole.CONSULTA
                }
            ]

            for user_data in default_users:
                user_create = UserCreate(**user_data)
                self.create_user(user_create)
        finally:
            db.close()


# Instancia global del servicio de base de datos
db = DatabaseService()