from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware  # LOCAL USE ONLY
from Utils.tools import recompose_png_to_jpg, resizer, image_to_matrix
from Python_Library.library import MLP

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

    if ia == "rust":
        # Load Own model
        model = MLP([8, 3])
        model.load(r"./Data/models/model1.json")

        predictions = model.predict(array, True)
        prediction = max(predictions)
        prediction_index = predictions.index(prediction)
        res = {"title": "", "estimation": prediction*100, "image": f"data:image/jpeg;base64,{base64}"}

        # Churros
        if prediction_index == 0:
            res['title'] = "Churros"
        # Apple Candy
        if prediction_index == 1:
            res['title'] = "Pomme d'amour"
        # Cotton Candy
        if prediction_index == 2:
            res['title'] = "Barbe à Papa"
    else:
        # Load tensorflow model
        ...

    return res


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
