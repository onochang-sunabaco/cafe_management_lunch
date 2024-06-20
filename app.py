from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'cafe_management.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        stock_quantity = request.form['stock_quantity']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO PRODUCTS (name, category, price, stock_quantity) VALUES (?, ?, ?, ?)",
                       (name, category, price, stock_quantity))
        conn.commit()
        conn.close()
        return redirect(url_for('add_product'))
    return render_template('add_product.html')

# 商品一覧ページの表示
@app.route('/products')
def products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCTS")
    products = cursor.fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/add_inventory', methods=['GET', 'POST'])
def add_inventory():
    if request.method == 'POST':
        product_id = request.form['product_id']
        user_id = request.form['user_id']
        quantity = request.form['quantity']
        note = request.form['note']
        received_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO INVENTORY (product_id, user_id, quantity, received_date, note) VALUES (?, ?, ?, ?, ?)",
                       (product_id, user_id, quantity, received_date, note))
        conn.commit()
        conn.close()
        return redirect(url_for('add_inventory'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, name FROM PRODUCTS")
    products = cursor.fetchall()
    cursor.execute("SELECT user_id, username FROM USERS")
    users = cursor.fetchall()
    conn.close()
    return render_template('add_inventory.html', products=products, users=users)

@app.route('/inventory')
def inventory():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT i.inventory_id, p.name as product_name, u.username, i.quantity, i.received_date, i.note
    FROM INVENTORY i
    JOIN PRODUCTS p ON i.product_id = p.product_id
    JOIN USERS u ON i.user_id = u.user_id
    ORDER BY i.received_date DESC
    """)
    inventory_records = cursor.fetchall()
    conn.close()
    return render_template('inventory.html', inventory_records=inventory_records)

if __name__ == '__main__':
    app.run(debug=True)
