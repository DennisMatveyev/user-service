from fastapi import APIRouter, Depends

from utils import validate_token
from schemas.user import User


common_router = APIRouter()


@common_router.get('/say_hello')
async def say_hello(user: User = Depends(validate_token)):
    return {'message': f"Hello {user.name}"}
