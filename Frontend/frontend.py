import jwt
from datetime import datetime, timedelta
from config import CONFIG
from flask import Flask, render_template, request, redirect, flash, url_for, session
from notes_shim import (
    register_user,
    login_user,
    delete_user,
    add_product,
    delete_product,
    add_item_to_cart,
    view_cart,
    clear_cart,
    remove_item_from_cart,
    get_all_products,
)
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

app = Flask(__name__)
app.secret_key = "coronavirus6969"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        status_code = register_user(username, password, email)
        if status_code == 201:
            flash("Registration successful!", "success")
            return redirect(url_for("login"))
        else:
            flash("Registration failed. Please try again.", "danger")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        status_code, token = login_user(username, password)

        if status_code == 200:
            response = redirect(url_for("products"))
            response.set_cookie("jwt_token", token, httponly=True)
            flash("Login successful!", "success")
            if username == "admin" and password == "123":
                return redirect(url_for("admin_panel"))
            return response
        else:
            flash("Login failed. Please check your credentials.", "danger")
    return render_template("login.html")


@app.route("/products")
def products():

    if "user" not in session:
        flash("You need to log in to view this page.", "warning")
        return redirect(url_for("login"))
     
    products_data = get_all_products()
    
    if isinstance(products_data, dict) and "error" in products_data:
        flash(products_data["error"], "danger")  
        products_list = []  
    else:
        products_list = products_data 
    
   
    return render_template("products.html", products=products_list)


@app.route("/cart", methods=["GET", "POST"])
def cart():
    if 'cart_items' not in session:
        session['cart_items'] = []

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add_item":
            product_id = request.form["product_id"]
            quantity = int(request.form["quantity"])
            status_code = add_item_to_cart(product_id, quantity)
            if status_code == 200 or 302:
                flash("Item added to cart!", "success")

        elif action == "remove_item":
            item_id = request.form.get("itemss_id")  
            print(f"Removing item with Item ID: {item_id}")
            if item_id:
                status_code = remove_item_from_cart(item_id)
                if status_code == 200:
                    flash("Item removed from cart.", "info")
                else:
                    flash("Failed to remove item from cart.", "danger")
            else:
                flash("No item ID provided.", "warning")

        return redirect(url_for("cart"))

    cart_total = sum(item['quantity'] * item['unit_price'] for item in session['cart_items'])
    cart_items = view_cart()
    print(f"Cart items: {cart_items}") 
    return render_template("cart.html", cart_items=cart_items, cart_total=cart_total)


@app.route("/checkout")
def checkout():
    clear_cart()
    flash("Thank you for your purchase!", "success")
    return redirect(url_for("home"))

@app.route("/admin", methods=["GET", "POST"])
def admin_panel():
    if "user" not in session or session["user"] != "admin":
        flash("Unauthorized access!", "danger")
        return redirect(url_for("login"))
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add_product":
            name = request.form["name"]
            description = request.form["description"]
            price = float(request.form["price"])
            quantity = int(request.form["quantity"])
            add_product(name, description, price, quantity)
            flash("Product added successfully!", "success")
        elif action == "delete_product":
            product_id = int(request.form["product_id"])
            delete_product(product_id)
            flash("Product deleted successfully!", "success")
        elif action == "delete_user":
            user_id = int(request.form["user_id"])
            delete_user(user_id)
            flash("User deleted successfully!", "success")
    return render_template("admin.html")  



@app.route("/logout")
def logout():
    response = redirect(url_for("home"))
    response.delete_cookie("jwt_token")
    flash("Logged out successfully.", "info")
    return response

if __name__ == "__main__":
    app.run(host=CONFIG["frontend"]["listen_ip"], port=CONFIG["frontend"]["port"], debug=CONFIG["frontend"]["debug"])
