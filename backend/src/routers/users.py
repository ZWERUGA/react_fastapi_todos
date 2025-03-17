from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from models.tables import User as UserORM
from schemas.tokens import Token
from services.users import (
    authenticate_user,
    create_access_token,
    get_user,
    get_password_hash,
)
from database.database import SessionDep


ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter(prefix="/auth")


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    """
    Аутентификация пользователя.
    """
    user = authenticate_user(
        session=session, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
async def register(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    """
    Регистрация пользователя.
    """
    if get_user(form_data.username, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username is already registered...",
        )

    new_user = {
        "username": form_data.username,
        "hashed_password": get_password_hash(form_data.password),
    }

    new_user = UserORM(**new_user)
    session.add(new_user)
    session.commit()
    return {"message": "User was created..."}
