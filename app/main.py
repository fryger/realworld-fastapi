import uvicorn
from fastapi import FastAPI
from endpoints.users import userRouter, authRouter
from endpoints.profiles import profileRouter
from endpoints.articles import articleRouter

from database import engine, Base
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(authRouter)
app.include_router(userRouter)
app.include_router(profileRouter)
app.include_router(articleRouter)


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await app.db_connection.close()


@app.get("/")
def home():
    return "Home"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
