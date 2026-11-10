"""Sign up, sign in, sign out, and the dependency that finds the signed-in user."""

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.config import get_settings
from app.db import get_session
from app.models import Credentials, User, UserRead
from app.security import COOKIE_NAME, create_token, hash_password, read_token, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])

SessionDep = Annotated[Session, Depends(get_session)]

NOT_SIGNED_IN = HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Sign in to continue.")


def current_user(
    session: SessionDep,
    token: Annotated[str | None, Cookie(alias=COOKIE_NAME)] = None,
) -> User:
    user_id = read_token(token) if token else None
    user = session.get(User, user_id) if user_id else None
    if user is None:
        raise NOT_SIGNED_IN
    return user


CurrentUser = Annotated[User, Depends(current_user)]


def _set_session_cookie(response: Response, user: User) -> None:
    settings = get_settings()
    response.set_cookie(
        COOKIE_NAME,
        create_token(user.id),
        max_age=settings.access_token_minutes * 60,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="strict",
        path="/api",
    )


def _normalize(email: str) -> str:
    return email.strip().lower()


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def register(credentials: Credentials, session: SessionDep, response: Response) -> User:
    user = User(
        email=_normalize(credentials.email),
        password_hash=hash_password(credentials.password),
    )
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="An account with this email already exists."
        ) from None
    session.refresh(user)
    _set_session_cookie(response, user)
    return user


@router.post("/login", response_model=UserRead)
def login(credentials: Credentials, session: SessionDep, response: Response) -> User:
    user = session.exec(select(User).where(User.email == _normalize(credentials.email))).first()
    if not verify_password(user.password_hash if user else None, credentials.password):
        # Same answer for an unknown email and a wrong password.
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Wrong email or password.")
    assert user is not None
    _set_session_cookie(response, user)
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response) -> None:
    settings = get_settings()
    response.delete_cookie(
        COOKIE_NAME, path="/api", httponly=True, secure=settings.cookie_secure, samesite="strict"
    )


@router.get("/me", response_model=UserRead)
def me(user: CurrentUser) -> User:
    return user
