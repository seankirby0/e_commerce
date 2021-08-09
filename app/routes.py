from werkzeug import datastructures
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import RegisterForm, LoginForm, CreateProduct
from app.models import Cart, User, Product
from flask_login import login_required, login_user, logout_user

@app.route('/')
def home_page():  

    # title = 'The Shop'
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(username, email, password)
        new_user = User(username, email, password)

        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you for signing up {new_user.username}!', 'primary')
        return redirect(url_for('home_page'))

    return render_template('register.html', title='Register for The Shop', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username = username).first()

        if user is None or not user.check_password(password):
            flash('Incorrect Username/Password. Please enter again!', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        flash(f'You have succesfully logged in', 'success')
        return redirect(url_for('home_page'))


    return render_template(url_for('home_page'))


@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out', 'primary')
    return redirect(url_for('home_page'))


@app.route('/create_product', methods=['GET', 'POST'])
def create_product():
    form = CreateProduct()
    if form.validate_on_submit():
        product_name = form.product_name.data
        price = form.price.data
        image = form.image.data

        new_product = Product(product_name, price, image)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('home_page'))


    return render_template('create_product.html', form=form)

@app.route('/products', methods = ['GET', 'POST'])
def products():
    my_products=Product.query.all()


    return render_template('products.html', products = my_products)


@app.route('/add', methods=['POST'])
def add_to_cart(product_id):

    product_name = Product.query.filter(Product.id == product_id)
    cart_item = Cart(product=product_name)
    db.session.add(cart_item)
    db.session.commit()

    return render_template('home.html', product=products)

@app.route('/delete', methods = ['POST'])
def delete_from_cart(product_id):

    product_name = Product.query.filter(Product.id == product_id)
    cart_item = Cart(product=product_name)
    db.session.delete(cart_item)
    db.session.commit()

    return render_template('home.html', product=products)

@app.route('/clear', methods = ['POST'])
def clear_cart(product_id):

    product_name = Product.query.filter(Product.id == product_id)
    cart_item = Cart(product=product_name)
    db.session.delete(cart_item)
    db.session.commit()

    return render_template('home.html', product=products)
