from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, logout_user, current_user, login_required, LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'noggers123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

#Product model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    cart = db.relationship('CartItem', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'
    
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f'<CartItem {self.id} - Product {self.product_id}>'

#Authentication loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Login route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    user = User.query.filter_by(username=username, password=password).first()
    
    if user:
        login_user(user)
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

#Cart route
@app.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    user = User.query.get_or_404(current_user.id)
    product = Product.query.get_or_404(product_id)
    cart_item = CartItem(user_id=int(current_user.id), product_id=int(product.id))
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({"message": "Product added to cart sucessfully!"}), 200

@app.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not cart_item:
        return jsonify({"message": "Item not found in cart."}), 404
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Product removed from cart successfully!"}), 200

@app.route('/api/cart', methods=['GET'])
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    products = []
    for item in cart_items:
        product = Product.query.get(item.product_id)
        if product:
            products.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description
            })
    return jsonify(products), 200

@app.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return jsonify({"message": "Your cart is empty"}), 400
    
    # Here you would typically process the payment and create an order
    # For simplicity, we will just clear the cart
    for item in cart_items:
        db.session.delete(item)
    
    db.session.commit()
    return jsonify({"message": "Checkout successful, your cart is now empty"}), 200

#Add product
@app.route('/api/products/add', methods=['POST'])
@login_required
def add_product():
    data = request.json
    if not data or not all(key in data for key in ('name', 'price')):
        return jsonify({"message": "Invalid product data"}), 400
    product = Product(
        name=data.get('name'),
        price=data.get('price'),
        description=data.get('description')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"}), 201

#GET all products
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description
    } for product in products]), 200

#GET by ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description
    }), 200

#UPDATE
@app.route('/api/products/update/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    data = request.json
    product = Product.query.get_or_404(product_id)
    
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']
    
    db.session.commit()
    return jsonify({"message": "Product updated successfully!"}), 200

#DELETE
@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully!"}), 200

# Define a simple route
@app.route('/')
def home():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)