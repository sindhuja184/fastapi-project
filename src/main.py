from typing import Union
from fastapi import FastAPI
from api.events.routing import router as event_router
from contextlib import asynccontextmanager
from api.db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(event_router, prefix = '/api/events')


# @app.on_event("startup")
# def on_startup():
#     print("init for db")
    
#api/events/
@app.get("/")
def read_root():
    return {"Hello":"world"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q : Union[str, None] = None):
    return {"item_id": item_id, "q" : q}

@app.get('/health')
def read_api_health():
    return {"status":"ok"}