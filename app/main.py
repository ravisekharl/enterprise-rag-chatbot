from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
 
from app.routes import router
from app.config import APP_NAME, APP_VERSION
 
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)
 
app.add_middleware(
    SessionMiddleware,
    secret_key="enterprise-rag-secret-key"
)
 
app.mount("/static", StaticFiles(directory="static"), name="static")
 
app.include_router(router)



