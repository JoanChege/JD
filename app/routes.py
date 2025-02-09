from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User, Product, Category, Subcategory

@app.route('/')
def index():
    categories= Category.query.all()
    return render_template('index.html', categories=categories)

@app.route('/category/<int:category_id>')
def category(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template('category.html', category=category)

@app.route('/subcategory/<int:subcategory_id>')
def subcategory(subcategory_id):
    subcategory = Subcategory.query.get_or_404(subcategory_id)
    return render_template('subcategory.html', subcategory=subcategory)

@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/cart')
@login_required
def cart():
    return render_template('cart.html')

@app.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic
        pass
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration logic
        pass
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/search')
def search():
    q = request.args.get('q') 
    if q:
        products = Product.query.filter(Product.name.ilike(f"%{q}%")).all() 
    else:
        products = Product.query.all() 
    return render_template('search_results.html', products=products, query=q) 
