from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
bootstrap = Bootstrap5(app)

# Налаштування Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {os.environ.get("ADMIN_LOGIN"): {'password': generate_password_hash(os.environ.get("ADMIN_PASSWORD"))}}


@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None


# Клас користувача для Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id


@app.context_processor
def inject_admin_phone():
    return {'ADMIN_PHONE_NUM': os.environ.get("ADMIN_PHONE")}


class MyDataRequired(DataRequired):
    def __init__(self, message=None):
        if not message:
            message = 'Це поле обов\'язкове для заповнення'
        super(MyDataRequired, self).__init__(message=message)


class LoginForm(FlaskForm):
    login = StringField('Логін', validators=[MyDataRequired()], render_kw={"placeholder": "name@example.com"})
    password = PasswordField('Пароль', validators=[MyDataRequired()], render_kw={"placeholder": "Пароль"})
    remember_me = BooleanField('Запам\'ятати мене')
    submit = SubmitField('Увійти')


@app.route("/")
def home():
    return render_template("index.html", active_page='home')


@app.route("/cars/")
def all_cars():
    return render_template("cars.html", active_page='cars')


@app.route("/rules/")
def rules_n_terms():
    return render_template("rules.html", active_page='rules')


@app.route("/about/")
def about_us():
    return render_template("about_us.html", active_page='about')


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('all_cars'))
    form = LoginForm()
    if form.validate_on_submit():
        login_, password = form.data.get("login"), form.data.get("password")
        if login_ not in users:
            form.login.errors.append('Неправильний логін')
        elif not check_password_hash(users[login_]['password'], password):
            form.password.errors.append('Неправильний пароль')
        else:
            user = User(login_)
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('all_cars'))
    return render_template("login.html", form=form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
