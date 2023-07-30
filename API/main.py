from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # LOCAL USE ONLY
from Utils.tools import recompose_png_to_jpg, resizer, image_to_matrix

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    base64 = data['base64']
    ia = data['ia']
    color = data['color']
    size = int(data['size'])

    path = recompose_png_to_jpg(base64)
    resizer(path, size=(size, size))
    array = image_to_matrix(path, True if color == "l" else False)
    print(array)

    return {"message": "predict Churros", "percent": 100, "data": "base64"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
