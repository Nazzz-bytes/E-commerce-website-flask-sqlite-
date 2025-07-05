import sqlite3

def create_db():
    conn = sqlite3.connect('flaskshop.db')
    c = conn.cursor()

    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Create products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    ''')

    # Insert sample products (only run once)
    sample_products = [
        ("T-Shirt", 499.99, "Comfortable cotton T-shirt"),
        ("Sneakers", 1299.50, "Stylish running sneakers"),
        ("Backpack", 899.00, "Durable and spacious backpack")
    ]

    # Optional: Comment this if running multiple times to avoid duplicate entries
    c.executemany("INSERT INTO products (name, price, description) VALUES (?, ?, ?)", sample_products)

    conn.commit()
    conn.close()
    print("Database and tables created successfully with sample products.")

if __name__ == '__main__':
    create_db()
