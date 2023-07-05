import uvicorn
from fastapi import FastAPI
from endpoints.users import userRouter, authRouter
from database import create_database
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(authRouter)

create_database()


@app.get("/")
def home():
    return "Home"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
