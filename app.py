from flask import Flask, render_template, request, redirect, url_for
import sqlite3

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

if __name__ == '__main__':
    app.run(debug=True)
