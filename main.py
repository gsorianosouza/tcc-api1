from fastapi import FastAPI
from typing import Union

app = FastAPI();

@app.get("/")
def hello_world():
    return {"Hello": "World 😁"}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: Union[str, None] = None):
    return {
        "Item_id": item_id,
        "Query": q
    }