from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from core.config import settings
from api.api_v1.auth import router as auth_router
from api.api_v1.webchat import router as webchat_router
from websocket.websocket import router as websocket_router
#from api.api_v1.webchat import router as ws_router
from fastapi.middleware.cors import CORSMiddleware

from models.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    print("vvjhvj")
    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(
    auth_router,
    #prefix=settings.api.prefix,
)

app.include_router(
    webchat_router,
    #prefix=settings.api.prefix,
)

app.include_router(
    websocket_router,
    #prefix=settings.api.prefix,
)
