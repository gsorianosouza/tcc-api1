from fastapi import HTTPException
from sqlalchemy.orm import Session

from auth.utils.auth_utils import get_password_hash
from user.models.user import User
from user.schemas.user import UserCreate


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str, role: str):
    return db.query(User).filter(User.email == email, User.role == role).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=str(user.email),
        username=user.username,
        password=get_password_hash(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, current_user_id: int, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if db_user.id == current_user_id:
        raise HTTPException(status_code=401, detail="Não é permitido excluir o próprio usuário")
    
    if db_user:
        db.delete(db_user)
        db.commit()
    return
