import argparse
import sys
from notes_shim import (
    login_user,
    get_all_products,
    delete_user,
    get_product_by_id,
    delete_product,
)



TOKEN = None


def authenticate():
    """Authenticate the user and store the token ."""
    global TOKEN
    print("Please login to access the system.")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    result = login_user(username, password)
    
    if isinstance(result, dict) and "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)
    else:
        TOKEN = result
        print("Authentication successful!")


def display_product_list():
    """Display the list of products."""
    products = get_all_products(TOKEN)
    if isinstance(products, dict) and "error" in products:
        print(f"Error: {products['error']}")
    else:
        for product in products:
            print(
                f"ID: {product['id']} - Name: {product['name']} - Price: {product['price']} - Quantity: {product['quantity']}"
            )


def main():
    """Execute main function."""
    global TOKEN
    parser = argparse.ArgumentParser()
    operations = parser.add_mutually_exclusive_group(required=True)
    operations.add_argument("-l", "--list", action="store_true", help="List all products")
    operations.add_argument("-d", "--delete", action="store_true", help="Delete a product")
    operations.add_argument("-du", "--deleteuser", action="store_true", help="Delete a user")
    operations.add_argument("-g", "--get", action="store_true", help="Get a product by ID")

    parser.add_argument("-i", "--id", type=int, help="Product or User ID")
    parser.add_argument("-n", "--name", help="Product name")
    parser.add_argument("-desc", "--description", help="Product description")
    parser.add_argument("-p", "--price", type=float, help="Product price")
    parser.add_argument("-q", "--quantity", type=int, help="Product quantity")

    arguments = parser.parse_args()

    if not TOKEN:
        authenticate()

    if arguments.list:
        display_product_list()

    if arguments.delete:
        if arguments.id:
            status_code = delete_product(arguments.id, TOKEN)
            if status_code == 200:
                print("Product deleted successfully!")
            else:
                print(f"Failed to delete product. Response: {status_code}")
        else:
            print("To delete a product, you must provide the product ID.")

    if arguments.deleteuser:
        if arguments.id:
            status_code = delete_user(arguments.id, TOKEN)
            if status_code == 200:
                print("User deleted successfully!")
            else:
                print(f"Failed to delete user. Response: {status_code}")
        else:
            print("To delete a user, you must provide the user ID.")

    if arguments.get:
        if arguments.id:
            result = get_product_by_id(arguments.id, TOKEN)
            if isinstance(result, dict) and "error" in result:
                print(result["error"])
            else:
                print(f"Product details: {result}")
        else:
            print("To get a product, you must provide the product ID.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
