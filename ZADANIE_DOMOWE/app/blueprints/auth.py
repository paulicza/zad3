from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('tasks.list_tasks'))
    return render_template('register.html', form=form)

@auth_bp.route('/log_in', methods=['GET', 'POST'])
def log_in():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):  
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('tasks.list_tasks'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('tasks.index'))
