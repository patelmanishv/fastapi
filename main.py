from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Welcome to FastAPI!</h1>"

import json
from typing import Optional
from pydantic import BaseModel

ITEMS_FILE = "items.json"

def load_items():
    try:
        with open(ITEMS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_items(items):
    with open(ITEMS_FILE, "w") as f:
        json.dump(items, f)

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

items_db = load_items()

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    item_dict["price_with_tax"] = item.price + (item.tax or 0)
    items_db.append(item_dict)
    save_items(items_db)
    return item_dict

@app.get("/items")
async def get_items():
    return items_db

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id < len(items_db):
        return items_db[item_id]
    return {"error": "Item not found"}