import sqlite3
from config import CONFIG

class EcommerceDB:
    @staticmethod
    def initialize(database_connection: sqlite3.Connection):
        cursor = database_connection.cursor()

        try:
            print("Dropping existing tables (if present)...")
            cursor.execute("DROP TABLE IF EXISTS cart")
            cursor.execute("DROP TABLE IF EXISTS product")
            cursor.execute("DROP TABLE IF EXISTS user")
        except sqlite3.OperationalError as db_error:
            print(f"Unable to drop table. Error: {db_error}")
        
        print("Creating tables...")
        cursor.execute(EcommerceDB.CREATE_PRODUCT_TABLE)
        cursor.execute(EcommerceDB.CREATE_USER_TABLE)
        cursor.execute(EcommerceDB.CREATE_CART_TABLE)
        
        database_connection.commit()
        print("Tables created successfully.")

        print("Populating database with sample data...")
        cursor.executemany(EcommerceDB.INSERT_PRODUCT, EcommerceDB.sample_products)
        cursor.executemany(EcommerceDB.INSERT_USER, EcommerceDB.sample_users)
        cursor.executemany(EcommerceDB.INSERT_CART, EcommerceDB.sample_carts)

        database_connection.commit()
        print("Sample data inserted successfully.")

    CREATE_PRODUCT_TABLE = """
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL
    );
    """

    CREATE_USER_TABLE = """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    """

    CREATE_CART_TABLE = """
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL CHECK (quantity = 1), 
        FOREIGN KEY (user_id) REFERENCES user (id),
        FOREIGN KEY (product_id) REFERENCES product (id),
        UNIQUE (user_id, product_id) 
    );
    """

    INSERT_PRODUCT = "INSERT INTO product (name, description, price, quantity) VALUES (?, ?, ?, ?)"
    INSERT_USER = "INSERT INTO user (username, password, email) VALUES (?, ?, ?)"
    INSERT_CART = "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)"

    sample_products = [
        ("Biology Notes", "notes for biology", 9.99, 50),
        ("Chemistry Notes", "notes for chemistry", 8.99, 60),
        ("Physics Notes", "notes for physics", 10.99, 40)
    ]

    sample_users = [
        ("talal", "123", "talal@gmail.com"),
        ("admin", "123", "admin@gmail.com")
    ]

    
    sample_carts = [
        (1, 1, 1),  # User 1, 1 Biology Note
        (1, 2, 1),  # User 1, 1 Chemistry Note
        (2, 3, 1)   # User 2, 1 Physics Note
    ]

def try_create_database():
    """Execute main function."""
    db_conn = sqlite3.connect(CONFIG["database"]["name"])
    db_conn.row_factory = sqlite3.Row

    EcommerceDB.initialize(db_conn)
    db_conn.close()

    print("Database creation finished!")    

    return 0
