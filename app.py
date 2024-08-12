# app.py
from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

# 加載 .env 文件中的環境變量
load_dotenv()

app = Flask(__name__)

# MySQL 配置
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('cartPage.html')

@app.route('/products', methods=['GET'])
def get_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()
    return jsonify(products)

@app.route('/cart', methods=['GET'])
def get_cart():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM cart")
    cart = cur.fetchall()
    cur.close()
    return jsonify(cart)

@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO cart (product_id, quantity) VALUES (%s, %s)", (product_id, quantity))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Product added to cart'})

if __name__ == '__main__':
    app.runapp.run(debug=True, use_reloader=True)