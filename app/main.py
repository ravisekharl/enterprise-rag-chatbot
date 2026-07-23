from fastapi import FastAPI
from app.config import APP_NAME, APP_VERSION
from fastapi.staticfiles import StaticFiles
from app.routes import router


app = FastAPI(title=APP_NAME,
              version=APP_VERSION)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)



