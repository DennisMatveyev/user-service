from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status

from crud.users import fetch_user, fetch_users, update_user
from db.db_setup import get_db
from schemas.user import User, UserUpdate


users_router = APIRouter()


@users_router.get('', response_model=List[User])
async def get_users(
    offset: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return fetch_users(db, offset=offset, limit=limit)


@users_router.get('/{user_id}', response_model=User)
async def get_user(
    user_id: int = Path(..., description='ID of User you want to get'),
    db: Session = Depends(get_db)
):
    user = fetch_user(db, user_id)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'User not found')

    return user


@users_router.patch('/{user_id}', response_model=User)
async def patch_user(
    data: UserUpdate,
    user_id: int = Path(..., description='ID of User you want to update'),
    db: Session = Depends(get_db)
):
    db_user = fetch_user(db, user_id)

    if db_user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'User not found')

    updated_user = update_user(db, db_user, data)

    return updated_user
