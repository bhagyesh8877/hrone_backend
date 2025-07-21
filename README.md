# HROne Backend Task – FastAPI + MongoDB

A backend system to manage **Products** and **Orders** using FastAPI and MongoDB.

---

## Tech Stack

- **FastAPI**
- **MongoDB** (via `pymongo`)
- **Pydantic** for data validation
- **Render** (or **localhost**) for deployment

---

## Project Structure

![alt text](image.png)

---

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server Locally
```bash
uvicorn app.main:app --reload
```

### 3. Connect MongoDB
Edit your `app/db.py`:
```python
from pymongo import MongoClient

### Replace Your username, password and cluster name in the following url
client = MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/")

### 4. Include your table name below which consist of two collections named produts and orders. In my case it is "task"
db = client["task"] 
```

---

## MongoDB Structure 

###  `products`
```json
{
  "_id": ObjectId,
  "name": "string",
  "description": "string",
  "price": float,
  "sizes": [
    {
      "size": "string",
      "quantity": int
    }
  ]
}

```

### `orders`
```json
{
  "_id": ObjectId,
  "userId": "string",
  "items": [
    {
      "productId": ObjectId,
      "qty": int
    }
  ]
}

```

---

## API Endpoints

> Base URL:
> ```
> https://bhagyesh-backend-task.onrender.com
> ```

---

### POST `/products`
**Create a product**
```json
POST /products
{
  "name": "T-Shirt",
  "description": "Basic cotton tee",
  "price": 299.99,
  "sizes": [
    { "size": "M", "quantity": 5 }
  ]
}
```
**Response:**
```json
{
  "_id": "66a9a1f4e93b8c56f1c0a001",
  "name": "T-Shirt",
  "description": "Basic cotton tee",
  "price": 299.99,
  "sizes": [
    { "size": "M", "quantity": 5 }
  ]
}
```

---

### GET `/products`
**List products (filter by name, size, and paginate)**
```
GET /products?name=shirt&size=M&limit=5&offset=0
```
**Response:**
```json
{
  "data": [
    {
      "id": "66a9a1f4e93b8c56f1c0a001",
      "name": "T-Shirt",
      "price": 299.99
    }
  ],
  "page": {
    "next": "5",
    "limit": 5,
    "previous": 0
  }
}
```

---

### POST `/orders`
**Create an order**
```json
POST /orders
{
  "userId": "user_1",
  "items": [
    {
      "productId": "66a9a1f4e93b8c56f1c0a001",
      "qty": 2
    }
  ]
}
```
**Response:**
```json
{
  "id": "66a9b2a1e93b8c56f1c0b001"
}
```

---

### GET `/orders`
**List orders with joined product details**
```
GET /orders?userId=user_1&limit=5&offset=0
```
**Response:**
```json
{
  "data": [
    {
      "id": "66a9b2a1e93b8c56f1c0b001",
      "items": [
        {
          "productDetails": {
            "id": "66a9a1f4e93b8c56f1c0a001",
            "name": "T-Shirt"
          },
          "qty": 2
        }
      ]
    }
  ],
  "page": {
    "next": "5",
    "limit": 5,
    "previous": 0
  }
}
```

---

## 👨‍💻 Author

**Bhagyesh Sunil Chaudhari**  