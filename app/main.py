# from typing import Union
from datetime import date
import os.path
from enum import Enum
from fastapi import FastAPI, Query, Response
from pydantic import BaseModel
from app.TodoJournal import TodoJournal


"""class TodoStr(BaseModel):
    todo: str
    # index: int | None = None
"""

class TodoIn(BaseModel):
    title: str
    text: str | None = None
    date_expire: str | None = None


class TodoOut(TodoIn):
    ID: int = 0
    date_created: str = date.today()



class TodoJrnl(BaseModel):
    path: str
    name: str | None = Query(default=None, min_length=3, max_length=50)
    todos: list[TodoOut] | None = None

    class Config:
        schema_extra = {
            "example": {
                "path": "testlist",
                "name": "My awesome todo list",
                "todos": [
                    {
                        "todo": "useless string1"
                    },
                    {
                        "todo": "useless string2"
                    }, {
                        "todo": "useless string3"
                    }
                ]
            }

        }


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


@app.get("/items_of_fake_db/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


@app.post("/todo/create")
async def create_todo(obj: TodoJrnl):
    TodoJournal.create(obj.path, obj.name)
    file = TodoJournal(obj.path)
    if obj.todos is not None:
        for i in obj.todos:
            file.add_todo(i.title)
    return {"Created todo": obj.name, "at": obj.path}


@app.post("/todo/add", response_model=TodoOut, response_model_include=["ID","date_created"])
async def add_todo(obj: TodoJrnl, elem: TodoIn):
    file = TodoJournal(obj.path)
    #kid = TodoOut(elem)
    #obj.todos.append(kid)
    file.add_todo(elem.title)
    return elem


@app.put("/todo/remove")
async def remove_todo(obj: TodoJrnl, elem: int):
    file = TodoJournal(obj.path)
    file.remove_todo(elem)
    return {"Removed todo": elem, ", from journal": obj.name}


@app.get("/todo/{todo_jrnl}", status_code=200)
async def show_todo_journal(todo_jrnl: str, response: Response):
    if not os.path.exists(todo_jrnl):
        response.status_code = 418
        return {"message": "TodoJournal's file not found, drink a tea instead"}
    file = TodoJournal(todo_jrnl)
    return {TodoJournal.print(file)}


@app.post("/todo/replace/{todo_jrnl}", status_code=200)
async def replace_todo(todo_jrnl: str, q: int, ent: TodoIn, response: Response):
    if not os.path.exists(todo_jrnl):
        response.status_code = 404
        return {"message": "TodoJournal's file not found"}
    file = TodoJournal(todo_jrnl)
    file.remove_todo(q)
    file.add_todo(TodoOut(ent).title)
    return {"Replaced todo with index": q, "to": ent, "in journal": todo_jrnl}


@app.post("/todo/properites_info", response_model=TodoOut, response_model_include=["ID","date_created"])
async def info_of_todo(todo_in: TodoIn):
    if todo_in.text is None:
        todo_in.text = "There was no text"
    if todo_in.date_expire is None:
        todo_in.date_expire = "There was no date of exp"
    return todo_in
