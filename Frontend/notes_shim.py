import json
import requests
from config import CONFIG
from flask import request

def get_headers():
    token = request.cookies.get("jwt_token")
    return {"Authorization": f"Bearer {token}"} if token else {}
def get_all_products():
    try:
        response = requests.get(f"{CONFIG['api']['url']}/admin_routes/products", headers=get_headers())
       
        if response.status_code == 200:
            print(f"Fetched products successfully: {response.json()}")
            return response.json()
        elif response.status_code == 404:
            print("No products found.")
            return {"error": "No products found"}, 404
        else:
            print(f"Failed to fetch products. Status code: {response.status_code}")
            return {"error": "Failed to fetch products"}, response.status_code
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while communicating with the API: {e}")
        return {"error": str(e)}, 500
    
def register_user(username, password, email):
    new_user = {
        "username": username,
        "password": password,
        "email": email
    }
    response = requests.post(f"{CONFIG['api']['url']}/admin_routes/register", json=new_user)
    return response.status_code

def login_user(username, password):
    credentials = {
        "username": username,
        "password": password
    }
    print(f"Sending login request with credentials: {credentials}")  
    response = requests.post(f"{CONFIG['api']['url']}/admin_routes/login", json=credentials)
    print(f"API response: {response.status_code}, {response.json()}")  
    
    if response.status_code == 200:
        
        token = response.json().get('token')
        return response.status_code, token 
    else:
        return response.status_code, None  



def delete_user(user_id):
    response = requests.delete(f"{CONFIG['api']['url']}/admin_routes/users/{user_id}", headers=get_headers())
    return response.status_code


def get_product_by_id(product_id):
    response = requests.get(f"{CONFIG['api']['url']}/admin_routes/products/{product_id}", headers=get_headers())
    return response.status_code

def add_product(name, description, price, quantity):
    new_product = {
        "name": name,
        "description": description,
        "price": price,
        "quantity": quantity
    }
    response = requests.post(f"{CONFIG['api']['url']}/admin_routes", json=new_product, headers=get_headers())
    return response.status_code

def delete_product(product_id):
    response = requests.delete(f"{CONFIG['api']['url']}/admin_routes/{product_id}", headers=get_headers())
    return response.status_code


def add_item_to_cart(product_id, quantity):
    
    cart_response = requests.get(f"{CONFIG['api']['url']}/admin_routes/cart")
    if cart_response.status_code == 200:
        cart = cart_response.json()
        if cart:  
            return {"message": "You can only have one product in the cart."}, 400

    item = {
        "product_id": product_id,
        "quantity": quantity
    }
    response = requests.post(f"{CONFIG['api']['url']}/admin_routes/cart", json=item, headers=get_headers())
    return response.status_code

def view_cart():
    response = requests.get(f"{CONFIG['api']['url']}/admin_routes/cart", headers=get_headers())
    return response.json()

def clear_cart():
    response = requests.delete(f"{CONFIG['api']['url']}/admin_routes/cart,", headers=get_headers())
    return response.status_code

def remove_item_from_cart(product_id):
    response = requests.post(f"{CONFIG['api']['url']}/admin_routes/cart/{product_id}")
    return response.status_code



