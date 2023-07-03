import uvicorn
from fastapi import FastAPI
from routes import defaultRouter

app = FastAPI()

app.include_router(defaultRouter)


@app.get("/")
def home():
    return "Home"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
