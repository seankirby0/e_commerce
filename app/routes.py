from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import RegisterForm, LoginForm
from app.models import User
from flask_login import login_required, login_user, logout_user

@app.route('/')
def home_page():
    # title = 'The Shop'
    return "Welcome to The Shop"

@app.route('/register' methods=['GET', 'POST'])
def register():
    form = RegisterForm
    if form.validate_on_submit():
        print('THE FORM IS VALID!!!')
        username = form.username.data
        email = form.email.data
        password = form.password.data
        print(username, email, password)
        new_user = User(username, email, password)

        db.session.add(new_user)
        db.session.commit()

        flash(f'Thank you for signing up {new_user.username}!', 'primary')
        return redirect(url_for('home_page'))

    return render_template('register.html', title='Register for The Shop', form = form)

@app.route('/login' methods=['GET', 'POST'])
def login():
    form = LoginForm
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
    return redirect(url_for('index'))

