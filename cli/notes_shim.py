import json
import requests
from config import CONFIG

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


def get_all_products(token):
    headers = {"Authorization": f"Bearer {token[1]}"}
    print(f"the header is: {headers}") 
    try:
        response = requests.get(f"{CONFIG['api']['url']}/admin_routes/products", headers=headers)
        print(f"Response status: {response.status_code}, Response text: {response.text}") 
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "No products found"}
        else:
            return {"error": f"Failed to fetch products. Status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def delete_user(user_id, token):
    try:
        headers = {"Authorization": f"Bearer {token[1]}"}
        response = requests.delete(f"{CONFIG['api']['url']}/admin_routes/users/{user_id}", headers=headers)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_product_by_id(product_id, token):
    try:
        headers = {"Authorization": f"Bearer {token[1]}"}
        response = requests.get(f"{CONFIG['api']['url']}/admin_routes/products/{product_id}", headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "Product not found"}
        else:
            return {"error": f"Failed to fetch product. Status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def add_product(name, description, price, quantity, token):
    new_product = {
        "name": name,
        "description": description,
        "price": price,
        "quantity": quantity,
    }
    try:
        headers = {"Authorization": f"Bearer {token[1]}"}
        response = requests.post(f"{CONFIG['api']['url']}/admin_routes/products", json=new_product, headers=headers)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def delete_product(product_id, token):
    try:
        headers = {"Authorization": f"Bearer {token[1]}"}
        response = requests.delete(f"{CONFIG['api']['url']}/admin_routes/products/{product_id}", headers=headers)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
