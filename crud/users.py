from typing import Optional, List

from sqlalchemy.orm import Session

from utils import hash_password
from db.models.user import User
from schemas.user import UserCreate, UserUpdate


def fetch_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def fetch_user_by_credentials(db: Session, name: str, password: str) -> Optional[User]:
    # TODO: implement real password hashing and verification
    db_user = db.query(User).filter(
        User.name == name,
        User.password == hash_password(password)
    ).first()

    return db_user


def fetch_users(db: Session, offset: int = 0, limit: int = 10) -> List[User]:
    return db.query(User).offset(offset).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    # TODO: implement real password hashing and verification
    fake_hashed_password = hash_password(user.password)
    db_user = User(name=user.name, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    data_dict = data.dict(exclude_unset=True)

    for key, value in data_dict.items():
        setattr(user, key, value)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
