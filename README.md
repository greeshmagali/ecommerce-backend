# 🛒 E-Commerce Backend API

A secure RESTful E-Commerce Backend API built using **Python, Flask, SQLAlchemy, SQLite, and JWT authentication**.

This project provides APIs for user authentication, product and category management, shopping carts, and order placement. It also implements **role-based authorization**, where administrators can manage products and categories while customers can manage their own carts and orders.

## 🚀 Features

* User signup and login
* Password hashing using Werkzeug
* JWT-based authentication
* Role-based authorization
* Admin-only product management
* Admin-only category management
* Product search and filtering
* Pagination for products
* Shopping cart management
* Stock validation
* Order placement
* Automatic order total calculation
* User-specific cart access
* User-specific order access
* RESTful API design
* SQLite database using SQLAlchemy ORM

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **Flask-SQLAlchemy**
* **Flask-JWT-Extended**
* **SQLite**
* **SQLAlchemy ORM**
* **Werkzeug**
* **Postman** for API testing
* **Git & GitHub**

## 📁 Project Structure

```text
ecommerce-backend/
│
├── app.py
├── config.py
├── models.py
├── utils.py
├── requirements.txt
├── .gitignore
│
└── routes/
    ├── auth.py
    ├── product_routes.py
    ├── category_routes.py
    ├── cart_routes.py
    └── place_order_routes.py
```

## 🔐 Authentication & Authorization

The API uses **JWT (JSON Web Token)** authentication.

After login, the user receives a JWT token. Protected endpoints require this token in the request header:

```text
Authorization: Bearer <your_token>
```

### User Roles

There are two roles:

* **Customer** – can view products, manage their own cart, and place/view their own orders.
* **Admin** – can create, update, and delete products and categories.

New users are registered as customers by default.

## 📌 API Endpoints

### Authentication

| Method | Endpoint   | Description                  | Authentication |
| ------ | ---------- | ---------------------------- | -------------- |
| POST   | `/signup`  | Register a new user          | No             |
| POST   | `/login`   | Login and receive JWT        | No             |
| GET    | `/profile` | Get logged-in user's profile | JWT            |

### Products

| Method | Endpoint         | Description       | Access |
| ------ | ---------------- | ----------------- | ------ |
| POST   | `/products`      | Create product    | Admin  |
| GET    | `/products`      | Get products      | Public |
| GET    | `/products/<id>` | Get product by ID | Public |
| PUT    | `/products/<id>` | Update product    | Admin  |
| DELETE | `/products/<id>` | Delete product    | Admin  |

Products can also be filtered and paginated using query parameters.

Example:

```text
GET /products?name=phone
```

### Categories

| Method | Endpoint           | Description     | Access |
| ------ | ------------------ | --------------- | ------ |
| POST   | `/categories`      | Create category | Admin  |
| GET    | `/categories`      | Get categories  | Public |
| PUT    | `/categories/<id>` | Update category | Admin  |
| DELETE | `/categories/<id>` | Delete category | Admin  |

### Cart

| Method | Endpoint          | Description                | Authentication |
| ------ | ----------------- | -------------------------- | -------------- |
| POST   | `/carts`          | Add product to cart        | JWT            |
| GET    | `/cart`           | View logged-in user's cart | JWT            |
| PUT    | `/cart/item/<id>` | Update cart item quantity  | JWT            |
| DELETE | `/cart/item/<id>` | Remove cart item           | JWT            |

The user ID is obtained from the JWT token instead of being supplied by the client.

### Orders

| Method | Endpoint       | Description                  | Authentication |
| ------ | -------------- | ---------------------------- | -------------- |
| POST   | `/order/place` | Place an order               | JWT            |
| GET    | `/orders`      | View logged-in user's orders | JWT            |
| GET    | `/order/<id>`  | View a specific order        | JWT            |

When an order is placed:

1. Cart items are checked.
2. Product stock is verified.
3. Order total is calculated.
4. Order and order items are created.
5. Product stock is reduced.
6. The cart is cleared.

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/greeshmagali/ecommerce-backend.git
```

### 2. Move into the project

```bash
cd ecommerce-backend
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

## 🧪 Testing with Postman

The API can be tested using Postman.

### Step 1: Register

```http
POST /signup
```

Example JSON:

```json
{
    "username": "testuser",
    "password": "123456"
}
```

### Step 2: Login

```http
POST /login
```

Example:

```json
{
    "username": "testuser",
    "password": "123456"
}
```

Copy the JWT token returned by the API.

### Step 3: Use the JWT

For protected endpoints, add:

```text
Authorization: Bearer <JWT_TOKEN>
```

### Step 4: Test protected operations

You can then test:

```text
GET    /profile
POST   /carts
GET    /cart
PUT    /cart/item/<id>
DELETE /cart/item/<id>
POST   /order/place
GET    /orders
GET    /order/<id>
```

## 🔒 Security

The project includes several security measures:

* Passwords are hashed instead of stored as plain text.
* JWT authentication protects private endpoints.
* Users can access only their own cart and orders.
* Product and category modification requires admin authorization.
* New users are assigned the customer role by default.
* User identity is obtained from the JWT instead of trusting a user ID sent by the client.
* Sensitive local files and environment files are excluded using `.gitignore`.

## 🗄️ Database Models

The project uses SQLAlchemy ORM with models for:

* `User`
* `Product`
* `Category`
* `Cart`
* `CartItem`
* `Order`
* `OrderItem`

The application uses SQLite for local development.

## 📈 Future Improvements

Possible future improvements include:

* MySQL/PostgreSQL deployment
* Database migrations using Flask-Migrate
* Payment gateway integration
* Product image uploads
* Product reviews and ratings
* Order status tracking
* Email notifications
* Docker deployment
* Automated unit and API tests
* Production deployment

## 🎯 Project Purpose

This project was developed to strengthen practical knowledge of:

* Backend development with Flask
* REST API development
* SQL and relational databases
* ORM using SQLAlchemy
* Authentication and authorization
* JWT-based security
* Database relationships
* API testing
* Git and GitHub

## 👩‍💻 Author

**Greeshma Gali**

B.Tech – Computer Science & Engineering (AI & ML)

GitHub:
https://github.com/greeshmagali07
