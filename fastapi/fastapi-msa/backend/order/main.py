from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/orders")
def get_orders():
    users_response = requests.get("http://user-service:8000/users")
    users = users_response.json()["users"]

    products_response = requests.get("http://product-service:8000/products")
    products = products_response.json()["products"]

    return {"users": users, "products": products}
