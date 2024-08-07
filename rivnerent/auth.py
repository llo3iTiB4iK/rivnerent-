from flask import Blueprint, render_template, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm
from .models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.all_cars'))
    form = LoginForm()
    if form.validate_on_submit():
        login_, password = form.data.get("login"), form.data.get("password")
        users = {current_app.config['ADMIN_LOGIN']: {'password': current_app.config['ADMIN_PASSWORD']}}
        if login_ not in users:
            form.login.errors.append('Неправильний логін')
        elif not users[login_]['password'] == password:
            form.password.errors.append('Неправильний пароль')
        else:
            user = User(login_)
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.all_cars'))
    return render_template("login.html", form=form)


@auth_bp.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
