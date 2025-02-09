from flask import render_template, url_for, redirect, request, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from app import app, db
from flask_bcrypt import Bcrypt
from app.models import User, Product, Category, Subcategory
from forms import RegistrationForm, LoginForm

bcrypt = Bcrypt()

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

@app.before_first_request
def initialize_cart():
    session['cart'] = []
    
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    cart = session.get('cart', [])

    # Check if the product is already in the cart
    for item in cart:
        if item['id'] == product.id:
            item['quantity'] += 1
            session['cart'] = cart
            return jsonify({'message': 'Product quantity updated in cart!'})

    # If the product is not in the cart, add it
    cart.append({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'quantity': 1,
        'image': product.image
    })
    session['cart'] = cart
    return jsonify({'message': 'Product added to cart!'})

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    updated_cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = updated_cart
    return jsonify({'message': 'Product removed from cart!'})

@app.route('/update_cart/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    cart = session.get('cart', [])
    quantity = int(request.form['quantity'])

    for item in cart:
        if item['id'] == product_id:
            item['quantity'] = quantity
            break

    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    payment_method = request.form.get('payment_method')

    if payment_method == 'visa':
        # Simulate Visa payment processing
        card_number = request.form.get('card_number')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')

        # Validate card details (simplified for demonstration)
        if not (card_number and expiry_date and cvv):
            flash('Please fill in all card details.', 'danger')
            return redirect(url_for('checkout'))

        flash('Visa payment processed successfully!', 'success')

    elif payment_method == 'mpesa':
        # Simulate M-Pesa payment confirmation
        flash('M-Pesa payment confirmed!', 'success')

    # Clear the cart after successful payment
    session['cart'] = []
    return redirect(url_for('index'))

@app.route('/checkout')
@login_required
def checkout():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render_template('checkout.html', cart=cart, total=total)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create an instance of the login form
    if form.validate_on_submit():
        # Check if the user exists and the password is correct
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:  # In a real app, use password hashing!
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/search')
@login_required
def search():
    q = request.args.get('q') 
    if q:
        products = Product.query.filter(Product.name.ilike(f"%{q}%")).all() 
    else:
        products = Product.query.all() 
    return render_template('search_results.html', products=products, query=q) 
