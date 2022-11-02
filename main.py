from datetime import datetime
from random import randint
from pytz import utc
from fastapi import FastAPI
from StealApp.apis import trades_router
from StealApp.db import engine, populate_table
from sqlmodel import Session, SQLModel


app = FastAPI()
app.include_router(trades_router)


@app.on_event("startup")
async def startup_event():
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)
    populate_table()
