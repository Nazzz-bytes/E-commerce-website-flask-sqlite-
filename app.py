from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('flaskshop.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('flaskshop.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('products'))
        else:
            return "Invalid email or password."

    return render_template('login.html')


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Products (login required)
@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('flaskshop.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    items = c.fetchall()
    conn.close()
    return render_template('products.html', products=items)

# Add to Cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if 'cart' not in session:
        session['cart'] = []

    cart = session['cart']
    cart.append(product_id)
    session['cart'] = cart
    return redirect(url_for('view_cart'))

# View Cart
@app.route('/cart')
def view_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cart = session.get('cart', [])
    products = []

    if cart:
        conn = sqlite3.connect('flaskshop.db')
        c = conn.cursor()
        placeholders = ','.join(['?'] * len(cart))
        c.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", cart)
        rows = c.fetchall()
        conn.close()

        # Match product quantity (1 per ID) and keep order
        id_counts = {pid: cart.count(pid) for pid in set(cart)}
        for row in rows:
            pid = row[0]
            qty = id_counts[pid]
            products.append({
                'id': row[0],
                'name': row[1],
                'price': row[2],
                'qty': qty,
                'total': row[2] * qty
            })

    return render_template('cart.html', products=products)


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        if product_id in cart:
            cart.remove(product_id)
            session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/admin/add-product', methods=['GET', 'POST'])
def add_product():
    # Allow only logged-in users (for now)
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # If the form is submitted
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']

        # Save to the database
        conn = sqlite3.connect('flaskshop.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)", (name, price, description))
        conn.commit()
        conn.close()

        # After saving, go to the product listing
        return redirect(url_for('products'))

    # If GET request, show the form
    return render_template('add_product.html')

# Admin Dashboard: View all products
@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('flaskshop.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()

    return render_template('admin_dashboard.html', products=products)

# Delete a product
@app.route('/admin/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('flaskshop.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))




if __name__ == '__main__':
    app.run(debug=True)

