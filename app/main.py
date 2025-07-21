from fastapi import FastAPI
from app.routes import products, orders

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to HROne Backend Task"}


app.include_router(products.router)
app.include_router(orders.router)
