from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from crud.users import create_user, fetch_user_by_credentials
from utils import create_access_token
from db.db_setup import get_db
from schemas.auth import Token
from schemas.user import UserCreate, User as UserSchema, UserLogin


auth_router = APIRouter()


@auth_router.post(
    "/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED
)
async def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except IntegrityError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 'Provided name is already in use'
        )


@auth_router.post(
    "/signin", response_model=Token, status_code=status.HTTP_200_OK
)
async def sign_in(user: UserLogin, db: Session = Depends(get_db)):
    db_user = fetch_user_by_credentials(db, user.name, user.password)

    if db_user is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, 'Credentials are invalid'
        )

    access_token = create_access_token({'name': db_user.name})

    return {'access_token': access_token}
