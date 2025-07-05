File-by-File Explanation


app.py
  
Contains all Flask routes and app configuration.

Uses session to track logged-in user state.

Handles form submissions for login, registration, add product, delete product.


db.py

Defines and initializes the database schema.

Creates two tables: users and products.

Must be run once before running the app.


flaskshop.db

SQLite database storing:

Users (id, name, email, password)

Products (id, name, price, description)


templates/

HTML files with Jinja2 templating.

base.html is the reusable layout, extended by other pages.


static/styles.css

Optional stylesheet to style headers, forms, and layout.
