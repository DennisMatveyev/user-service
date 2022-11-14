import uvicorn
from fastapi import FastAPI

from db.db_setup import engine
from db.models import user
from routers.base import api_router


user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
