#from typing import Union
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from TodoJournal import TodoJournal


class TodoStr(BaseModel):
    todo: str
    #index: int | None = None


class TodoJrnl(BaseModel):
    path: str
    name: str
    todos: list[TodoStr] | None = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/items/{item_id}")
async def read_item(item_id: int | str = int, q: str | None = None):
    if item_id == "me":
        return "Hello there"

    return {"item_id": item_id, "q": q}


@app.get("/itemsss/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.post("/todo/create")
async def create_todo(obj: TodoJrnl):
    TodoJournal.create(obj.path, obj.name)
    file = TodoJournal(obj.path)
    if obj.todos is not None:
        for i in obj.todos:
            file.add_todo(i)
    return {"Created todo": obj.name, "at": obj.path}


@app.post("/todo/add")
async def add_todo(obj: TodoJrnl, elem: TodoStr):
    file = TodoJournal(obj.path)
    file.add_todo(elem)
    return {"Added todo: ": elem, ", to journal: ": obj.name}
