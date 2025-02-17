import logging
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Annotated, Optional

from fastapi import Depends, FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Session, SQLModel, create_engine
from starlette.middleware.cors import CORSMiddleware

from sms_processing import SmsData, SMSProcessor, get_all_sms

log_file = "unprocessed_sms.log"
# Looger configuration
logging.basicConfig(
    filename=log_file,
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

engine = create_engine(settings.DATABASE_URL, echo=False)


def get_database():
    with Session(engine) as session:
        yield session


database = Annotated[Session, Depends(get_database)]


@asynccontextmanager
@lru_cache(maxsize=200)
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="MOMO APP API",
    description="Backend for a MOMO wallet",
    lifespan=lifespan,
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
)


@app.get("/", tags=["SMS Processing"])
async def main(db: database):
    process = SMSProcessor(db=db).process_and_store_sms()
    return process


@app.get("/sms", tags=["SMS Processing"])
async def get_sms(
    db: database,
    search: Optional[str] = None,
    type: Optional[str] = None,
    date: Optional[str] = None,
    amount: Optional[str] = None,
):

    get_all = get_all_sms(db, search, type, date, amount)
    return get_all
