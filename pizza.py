from fastapi import FastAPI, Body, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI()

class Pizza :
    id : int
    name : str
    ingredients : list
    price : float
    quantity : int

    def __init__ (self, id, name, ingredients, price, quantity):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.price = price
        self.quantity = quantity

class PizzaRequest(BaseModel) :
    id : Optional[int] = None
    name : str = Field(min_length = 3)
    ingredients : list = Field(min_length = 1)
    price : float = Field(gt = 0)
    quantity : int = Field(gt = -1)

    class Config :
        json_schema_extra = {
            "example" : {
                "name" : "Margherita",
                "ingredients" : ["tomato", "mozzarella"],
                "price" : 5.99,
                "quantity" : 1
            }
        }

pizzas = [Pizza(1, "Margherita", ["tomato", "mozzarella"], 5.99, 1),
          Pizza(2, "Marinara", ["tomato", "garlic"], 4.99, 1),
          Pizza(3, "Quattro Stagioni", ["tomato", "mozzarella", "mushrooms", "ham", "olives"], 7.99, 1),
          Pizza(4, "Carbonara", ["tomato", "mozzarella", "eggs", "bacon"], 7.99, 1),
          Pizza(5, "Frutti di Mare", ["tomato", "mozzarella", "seafood"], 8.99, 1),
        ]

@app.get("/pizzas")
async def read_all_pizzas():
    return pizzas

@app.get("/pizzas/{pizza_id}")
async def get_pizza_by_id(pizza_id : int = Path(gt=0)) :
    for pizza in pizzas :
        if pizza.id == pizza_id :
            return pizza
    raise HTTPException(status_code=404, detail="Pizza not found")

@app.post("/pizzas")
async def add_pizza(pizza_request : PizzaRequest) :
    print(pizza_request)
    new_pizza = Pizza(**pizza_request.model_dump())
    new_pizza_with_id = find_id(new_pizza)
    pizzas.append(new_pizza_with_id)
    return pizzas

def find_id(pizza: Pizza):
    if len(pizzas) > 0 :
        pizza.id = pizzas[-1].id + 1
    else :
        pizza.id = 1
    return pizza

@app.put("/pizzas")
async def edit_pizza(pizza_request : PizzaRequest) :
    for pizza in pizzas :
        if pizza.id == pizza_request.id :
            pizza.name = pizza_request.name
            pizza.ingredients = pizza_request.ingredients
            pizza.price = pizza_request.price
            pizza.quantity = pizza_request.quantity
            return pizza
    raise HTTPException(status_code=404, detail="Pizza not found")

@app.delete("/pizzas/{pizza_id}")
async def delete_pizza(pizza_id : int = Path(gt=0)) :
    for pizza in pizzas :
        if pizza_id == pizza.id :
            pizzas.remove(pizza)
            return pizzas
    raise HTTPException(status_code=404, detail="Pizza not found")
