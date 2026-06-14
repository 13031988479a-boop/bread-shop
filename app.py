from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, template_folder='templates')


def get_db():
    conn = sqlite3.connect('bread_shop.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    sort = request.args.get('sort', 'default')
    conn = get_db()

    if sort == 'hot':
        products = conn.execute("SELECT * FROM products WHERE is_hot=1 ORDER BY id").fetchall()
    elif sort == 'new':
        products = conn.execute("SELECT * FROM products WHERE is_new=1 ORDER BY id").fetchall()
    elif sort == 'price_asc':
        products = conn.execute("SELECT * FROM products ORDER BY price ASC").fetchall()
    elif sort == 'price_desc':
        products = conn.execute("SELECT * FROM products ORDER BY price DESC").fetchall()
    else:
        products = conn.execute("SELECT * FROM products ORDER BY id").fetchall()

    conn.close()
    return render_template('index.html', products=products, sort=sort)


@app.route('/product/<int:id>')
def product(id):
    conn = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('product.html', product=product)


@app.route('/admin')
def admin():
    conn = get_db()
    products = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
    conn.close()
    return render_template('admin.html', products=products)


@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    category = request.form['category']
    is_hot = 1 if request.form.get('is_hot') else 0
    is_new = 1 if request.form.get('is_new') else 0

    conn = get_db()
    conn.execute('''
                 INSERT INTO products (name, description, price, category, is_hot, is_new)
                 VALUES (?, ?, ?, ?, ?, ?)
                 ''', (name, description, price, category, is_hot, is_new))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))


@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        category = request.form['category']
        is_hot = 1 if request.form.get('is_hot') else 0
        is_new = 1 if request.form.get('is_new') else 0

        conn.execute('''
                     UPDATE products
                     SET name=?,
                         description=?,
                         price=?,
                         category=?,
                         is_hot=?,
                         is_new=?
                     WHERE id = ?
                     ''', (name, description, price, category, is_hot, is_new, id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))
    else:
        product = conn.execute("SELECT * FROM products WHERE id=?", (id,)).fetchone()
        conn.close()
        return render_template('edit.html', product=product)


if __name__ == '__main__':
    app.run(debug=True, port=5000)#原地址
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)