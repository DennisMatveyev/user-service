from fastapi import APIRouter

from routers.auth import auth_router
from routers.common import common_router
from routers.users import users_router


api_router = APIRouter()
api_router.include_router(auth_router, prefix='', tags=['auth'])
api_router.include_router(common_router, prefix='', tags=['common'])
api_router.include_router(users_router, prefix='/users', tags=['users'])
