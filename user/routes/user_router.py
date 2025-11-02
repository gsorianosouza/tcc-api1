from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from auth.services.auth_service import get_current_active_user
from core.database import get_db
from user.models.user import User
from user.schemas.user import UserSchema, UserCreate
from user.services.user_service import get_users, create_user, get_user, delete_user

user_router = APIRouter(prefix='/users',tags=['Usuários'])

@user_router.get('/', response_model=list[UserSchema])
def user_list(db: Session = Depends (get_db), current_user: User = Depends(get_current_active_user)):
    db_users = get_users(db)

    return db_users


@user_router.get('/me', response_model=UserSchema)
def user_list(current_user: User = Depends(get_current_active_user)):
    return current_user



@user_router.get('/{user_id}', response_model=UserSchema)
def user_detail(user_id: int, db: Session = Depends (get_db), current_user: User = Depends(get_current_active_user)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado. Verifique o ID utilizado.")

    return db_user


@user_router.delete('/{user_id}')
def user_delete(user_id: int, db: Session = Depends (get_db), current_user: User = Depends(get_current_active_user)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado. Verifique o ID utilizado.")

    delete_user(db, current_user.id, db_user.id)
    return {"Mensagem": "Usuário apagado com sucesso"}


@user_router.post("/add", response_model=UserSchema)
def user_post(user: UserCreate, db:Session = Depends(get_db)):
    return create_user(db, user)
