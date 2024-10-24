from xml.sax.handler import version

from fastapi import FastAPI, APIRouter
import sqlite3
from routes.articles import router as articles_router
from routes.comments import router as comments_router

app = FastAPI(version="1.0", title="FastAPI Blog API", description="A simple blog API using FastAPI")
apiRouter = APIRouter(prefix="/v1")

apiRouter.include_router(articles_router)
apiRouter.include_router(comments_router)

app.include_router(apiRouter)