import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize sqlalchemy
db = SQLAlchemy(app)
# Initialize Marshmallow
ma = Marshmallow(app)


# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

    def __repr__(self):
        return "<Product {}>".format(self.name)


# Product schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')


# Initialize schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# Get all products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    return products_schema.jsonify(all_products)


# Get one product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Create a product
@app.route('/product', methods=['POST'])
def create_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product = Product(name, description, price, qty)
    db.session.add(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Delete a product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)


# Update a product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    product.name = request.json['name']
    product.description = request.json['description']
    product.price = request.json['price']
    product.qty = request.json['qty']

    db.session.commit()
    return product_schema.jsonify(product)


# Run server
if __name__ == '__main__':
    app.run(debug=True)
