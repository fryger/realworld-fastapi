import uvicorn
from fastapi import FastAPI
from endpoints.users import userRouter, authRouter
from database import create_database

app = FastAPI()

app.include_router(authRouter)
# app.include_router(userRouter)

create_database()


@app.get("/")
def home():
    return "Home"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
