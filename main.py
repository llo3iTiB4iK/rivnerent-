from flask import Flask, render_template, redirect, url_for, abort
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Enum, Text, Float, CheckConstraint
import enum
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
    def __init__(self, id_):
        self.id = id_


# Налаштування БД
class Base(DeclarativeBase):
    pass


# Підключення до БД
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Налаштування таблиці Автомобілів
class CarCategoryEnum(enum.Enum):
    econom = "Бюджетні"
    comfort = "Комфорт"
    crossover = "Кросовери"
    business = "Бізнес"
    premium = "Преміум 4х4"
    bus = "Мікроавтобуси"


class FuelTypeEnum(enum.Enum):
    petrol = "Бензин"
    gas = "Газ/Бензин"
    diesel = "Дизель"
    hybrid = "Гібрид"


class TransmissionEnum(enum.Enum):
    manual = "Механіка"
    automatic = "Автомат"


class Car(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    category: Mapped[CarCategoryEnum] = mapped_column(Enum(CarCategoryEnum), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    engine_size: Mapped[float] = mapped_column(Float, nullable=False)
    fuel_type: Mapped[FuelTypeEnum] = mapped_column(Enum(FuelTypeEnum), nullable=False)
    transmission: Mapped[TransmissionEnum] = mapped_column(Enum(TransmissionEnum), nullable=False)
    seats: Mapped[int] = mapped_column(Integer, CheckConstraint('seats > 0'), nullable=False)
    info_url: Mapped[str] = mapped_column(String(500), nullable=False)
    price_1to3: Mapped[str] = mapped_column(String(20), nullable=False)
    price_4to9: Mapped[str] = mapped_column(String(20), nullable=False)
    price_10to25: Mapped[str] = mapped_column(String(20), nullable=False)
    price_26to89: Mapped[str] = mapped_column(String(20), nullable=False)
    deposit: Mapped[str] = mapped_column(String(20), nullable=False)


# Створення БД (якщо не існує)
with app.app_context():
    db.create_all()


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
    result = db.session.execute(db.select(Car))
    cars = result.scalars().all()
    return render_template("cars.html", active_page='cars', cars=cars)


@app.route("/cars/<car_name>")
def show_car(car_name):
    try:
        car_id = int(car_name.split('_id')[-1])
    except ValueError:
        car_id = None
    car = db.get_or_404(Car, car_id)
    return render_template("car.html", active_page='cars', car=car)


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
