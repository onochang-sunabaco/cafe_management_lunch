from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
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
        flash('Product added successfully!')
        return redirect(url_for('products'))
    return render_template('add_product.html')

@app.route('/products')
def products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PRODUCTS")
    products = cursor.fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        stock_quantity = request.form['stock_quantity']
        
        cursor.execute("""
            UPDATE PRODUCTS 
            SET name = ?, category = ?, price = ?, stock_quantity = ?
            WHERE product_id = ?
        """, (name, category, price, stock_quantity, product_id))
        conn.commit()
        conn.close()
        flash('Product updated successfully!')
        return redirect(url_for('products'))
    
    cursor.execute("SELECT * FROM PRODUCTS WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM PRODUCTS WHERE product_id = ?", (product_id,))
    conn.commit()
    conn.close()
    flash('Product deleted successfully!')
    return redirect(url_for('products'))

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

@app.route('/edit_inventory/<int:inventory_id>', methods=['GET', 'POST'])
def edit_inventory(inventory_id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        product_id = request.form['product_id']
        user_id = request.form['user_id']
        quantity = request.form['quantity']
        note = request.form['note']
        received_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            UPDATE INVENTORY
            SET product_id = ?, user_id = ?, quantity = ?, note = ?, received_date = ?
            WHERE inventory_id = ?
        """, (product_id, user_id, quantity, note, received_date, inventory_id))
        conn.commit()
        conn.close()
        flash('Inventory record updated successfully!')
        return redirect(url_for('inventory'))

    cursor.execute("SELECT * FROM INVENTORY WHERE inventory_id = ?", (inventory_id,))
    inventory_record = cursor.fetchone()
    conn.close()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, name FROM PRODUCTS")
    products = cursor.fetchall()
    cursor.execute("SELECT user_id, username FROM USERS")
    users = cursor.fetchall()
    conn.close()
    
    return render_template('edit_inventory.html', inventory_record=inventory_record, products=products, users=users)

@app.route('/delete_inventory/<int:inventory_id>', methods=['POST'])
def delete_inventory(inventory_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM INVENTORY WHERE inventory_id = ?", (inventory_id,))
    conn.commit()
    conn.close()
    flash('Inventory record deleted successfully!')
    return redirect(url_for('inventory'))

if __name__ == '__main__':
    app.run(debug=True)
