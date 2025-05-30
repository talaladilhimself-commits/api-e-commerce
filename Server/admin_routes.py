import sqlite3
from flask import jsonify, request, Flask
from config import CONFIG
import jwt
from datetime import datetime, timedelta
app = Flask(__name__)
SECRET_KEY = "veryverysecretkey"

def encode_jwt(payload):
    payload["exp"] = datetime.utcnow() + timedelta(hours=2)  # Token expiry
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def auth_required(func):
    def wrapper(*args, **kwargs):
        from flask import request, jsonify
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401
        token = auth_header.split(" ")[1]
        user_data = decode_jwt(token)
        if not user_data:
            return jsonify({"error": "Invalid or expired token"}), 401
        return func(*args, **kwargs, user=user_data)
    return wrapper

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def get_db_connection():
    try:
        db_conn = sqlite3.connect(CONFIG["database"]["name"])
        db_conn.row_factory = dict_factory
        return db_conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None


def remove_item_from_cart(product_id):
    DELETE_ITEM = "DELETE FROM cart WHERE id = ?"
    db_conn = get_db_connection()
    if db_conn is None:
        return jsonify({"error": "Database connection error"}), 500

    try:
        with db_conn:
            cursor = db_conn.cursor()
            cursor.execute(DELETE_ITEM, (product_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": "Item not found"}), 404
        return jsonify({"message": "Item removed from cart"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400


def add_product():
    product_data = request.get_json()
    INSERT_PRODUCT = """
    INSERT INTO product (name, description, price, quantity)
    VALUES (?, ?, ?, ?)
    """
    db_conn = get_db_connection()
    if db_conn is None:
        return jsonify({"error": "Database connection error"}), 500

    try:
        with db_conn:
            cursor = db_conn.cursor()
            cursor.execute(INSERT_PRODUCT, (
                product_data["name"], 
                product_data["description"], 
                product_data["price"], 
                product_data["quantity"]
            ))
            new_product_id = cursor.lastrowid
        return jsonify({"product_id": new_product_id}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400



def delete_product(product_id):
    DELETE_PRODUCT = "DELETE FROM product WHERE id = ?"
    db_conn = get_db_connection()
    if db_conn is None:
        return jsonify({"error": "Database connection error"}), 500

    try:
        with db_conn:
            cursor = db_conn.cursor()
            cursor.execute(DELETE_PRODUCT, (product_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": "Product not found"}), 404
        return "Product deleted successfully", 204
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400

def get_product_by_id(product_id):
    SELECT_PRODUCT_BY_ID = "SELECT * FROM product WHERE id = ?"
    db_conn = get_db_connection()
    if db_conn is None:
        return jsonify({"error": "Database connection error"}), 500

    try:
        with db_conn:
            cursor = db_conn.cursor()
            cursor.execute(SELECT_PRODUCT_BY_ID, (product_id,))
            product = cursor.fetchone()
            if product is None:
                return jsonify({"error": "Product not found"}), 404
        return jsonify(product), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400


def get_all_products():
    SELECT_ALL_PRODUCTS = "SELECT * FROM product"
    db_conn = get_db_connection()
    if db_conn is None:
        return jsonify({"error": "Database connection error"}), 500

    try:
        with db_conn:
            cursor = db_conn.cursor()
            cursor.execute(SELECT_ALL_PRODUCTS)
            products = cursor.fetchall()
            if not products:
                return jsonify({"error": "No products found"}), 404
        return jsonify(products), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400




def delete_user(user_id):
    DELETE_USER = "DELETE FROM user WHERE id = ?"
    db_conn = get_db_connection()
    if db_conn is None:
        return jsonify({"error": "Database connection error"}), 500

    try:
        with db_conn:
            cursor = db_conn.cursor()
            cursor.execute(DELETE_USER, (user_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": "User not found"}), 404
        return "User deleted successfully", 204
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400
    
def register_user():
    user_data = request.get_json()
    INSERT_USER = """
    INSERT INTO user (username, password, email)
    VALUES (?, ?, ?)
    """
    db_conn = get_db_connection()
    if db_conn is None:
        return jsonify({"error": "Database connection error"}), 500

    try:
        with db_conn:
            cursor = db_conn.cursor()
            cursor.execute(INSERT_USER, (
                user_data["username"], 
                user_data["password"], 
                user_data["email"]
            ))
            new_user_id = cursor.lastrowid
        return jsonify({"user_id": new_user_id}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400
    

def login_user():
    login_data = request.get_json()
    SELECT_USER = """
    SELECT * FROM user WHERE username = ? AND password = ?
    """
    db_conn = get_db_connection()
    if db_conn is None:
        return {"error": "Database connection error"}, 500

    try:
        with db_conn:
            cursor = db_conn.cursor()
            cursor.execute(SELECT_USER, (
                login_data["username"],
                login_data["password"]
            ))
            user = cursor.fetchone()
            if user is None:
                return {"error": "Invalid username or password"}, 401

            token = encode_jwt({"user_id": user["id"], "username": user["username"]})
            return {"token": token}, 200
    except sqlite3.Error as e:
        return {"error": str(e)}, 400

    
def add_item_to_cart():
    item_data = request.get_json()
    SELECT_ITEM = "SELECT * FROM cart WHERE product_id = ?"
    db_conn = get_db_connection()
    if db_conn is None:
        return jsonify({"error": "Database connection error"}), 500

    try:
        with db_conn:
            cursor = db_conn.cursor()
            cursor.execute(SELECT_ITEM, (item_data["product_id"],))
            existing_item = cursor.fetchone()

            if existing_item:
                return jsonify({"message": "Item is already in the cart"}), 200
            else:
                INSERT_ITEM = """
                INSERT INTO cart (product_id, quantity)
                VALUES (?, ?)
                """
                cursor.execute(INSERT_ITEM, (
                    item_data["product_id"],
                    item_data["quantity"]
                ))
                new_item_id = cursor.lastrowid
                return jsonify({"item_id": new_item_id, "message": "Item added to the cart"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400

def clear_cart():
    DELETE_CART = "DELETE FROM cart"
    db_conn = get_db_connection()
    if db_conn is None:
        return jsonify({"error": "Database connection error"}), 500

    try:
        with db_conn:
            cursor = db_conn.cursor()
            cursor.execute(DELETE_CART)
        return jsonify({"message": "Cart cleared"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400

def view_cart():
    SELECT_CART = """
    SELECT 
        cart.id AS cart_id,
        product.name AS product_name,
        product.price AS product_price,
        product.id As product_id,
        cart.quantity AS cart_quantity,
        (product.price * cart.quantity) AS total_price
    FROM cart
    JOIN product ON cart.product_id = product.id
    """
    db_conn = get_db_connection()
    if db_conn is None:
        return jsonify({"error": "Database connection error"}), 500

    try:
        with db_conn:
            cursor = db_conn.cursor()
            cursor.execute(SELECT_CART)
            cart_items = cursor.fetchall()
        return jsonify([dict(item) for item in cart_items]), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 400


