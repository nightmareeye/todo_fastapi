from typing import Union
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from TodoJournal import TodoJournal


class Todo(BaseModel):
    path: str
    name: str
    todo: Union[str, None] = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: Union[int, str] = int, q: Union[str, None] = None):
    if item_id == "me":
        return "Hello there"

    return {"item_id": item_id, "q": q}


@app.post("/todo")
async def create_todo(obj: Todo):
    TodoJournal.create(obj.path, obj.name)
    return {"Created todo": obj.name, "at": obj.path}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/itemsss/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]
