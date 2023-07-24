from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # LOCAL USE ONLY
from pydantic import BaseModel

app = FastAPI()

# LOCAL USE ONLY - START
origins = [
    "http://localhost",
    "http://localhost:8100",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ImageData(BaseModel):
    base64: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    base64 = data['data']
    return {"message": "predict Churros", "percent": 100, "data": base64}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
