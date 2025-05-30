from fastapi import FastAPI
from app import database, models
from app.routes import router

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

app.include_router(router, prefix="/books", tags=["Books"])
