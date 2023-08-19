from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


products = [
    {"id": 1, "name": "Product 1"},
    {"id": 2, "name": "Product 2"},
    {"id": 3, "name": "Product 3"},
]


@app.get("/products")
def get_products():
    return {"products": products}
