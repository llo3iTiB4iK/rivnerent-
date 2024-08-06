import sqlalchemy.exc
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, URLField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, URL, NumberRange
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
        super().__init__(message=message)


class MyURL(URL):
    def __init__(self, message=None):
        if not message:
            message = 'Некоректне URL-посилання'
        super().__init__(message=message)


class LoginForm(FlaskForm):
    login = StringField('Логін', validators=[MyDataRequired()], render_kw={"placeholder": "name@example.com"})
    password = PasswordField('Пароль', validators=[MyDataRequired()], render_kw={"placeholder": "Пароль"})
    remember_me = BooleanField('Запам\'ятати мене')
    submit = SubmitField('Увійти')


class CarForm(FlaskForm):
    name = StringField('Марка, модель', validators=[MyDataRequired()], render_kw={"placeholder": "Audi A6 Allroad"})
    category = SelectField('Категорія', validators=[MyDataRequired()],
                           choices=[(alias, member.value) for alias, member in CarCategoryEnum.__members__.items()])
    img_url = URLField('Посилання на зображення', validators=[MyDataRequired(), MyURL()],
                       render_kw={"placeholder": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Audi_A6_Allroad_Quattro_C8_1X7A0301.jpg"})
    description = TextAreaField('Опис', validators=[MyDataRequired()], render_kw={"placeholder": "Надійний, елегантний універсал для подорожей з сім'єю."})
    engine_size = FloatField('Об\'єм двигуна (л)', validators=[MyDataRequired("Об'єм двигуна має бути задано у форматі числа з плаваючою крапкою"),
                                                               NumberRange(0, message="Літраж двигуна повинен перевищувати 0")], render_kw={"placeholder": "2.0"})
    fuel_type = SelectField('Тип пального', validators=[MyDataRequired()],
                           choices=[(alias, member.value) for alias, member in FuelTypeEnum.__members__.items()])
    transmission = SelectField('Тип КПП', validators=[MyDataRequired()],
                            choices=[(alias, member.value) for alias, member in TransmissionEnum.__members__.items()])
    seats = IntegerField('Кількість місць', validators=[MyDataRequired(), NumberRange(1, message="Авто повинне мати хоча б 1 місце")], render_kw={"placeholder": "5"})
    info_url = URLField('Посилання на детальні характеристики авто', validators=[MyDataRequired(), MyURL()],
                       render_kw={"placeholder": "https://audi-a6-allroad-quattro.infocar.ua/mod_14642_a6-allroad-quattro_id5893.html"})
    price_1to3 = StringField('Вартість за добу (термін прокату 1-3 діб)', validators=[MyDataRequired()], render_kw={"placeholder": "999 $"})
    price_4to9 = StringField('Вартість за добу (термін прокату 4-9 діб)', validators=[MyDataRequired()], render_kw={"placeholder": "999 $"})
    price_10to25 = StringField('Вартість за добу (термін прокату 10-25 діб)', validators=[MyDataRequired()], render_kw={"placeholder": "999 $"})
    price_26to89 = StringField('Вартість за добу (термін прокату 26-89 діб)', validators=[MyDataRequired()], render_kw={"placeholder": "999 $"})
    deposit = StringField('Розмір завдатку', validators=[MyDataRequired()], render_kw={"placeholder": "999 $"})
    submit = SubmitField('Зберегти')


@app.route("/")
def home():
    return render_template("index.html", active_page='home')


@app.route("/cars/")
def all_cars():
    result = db.session.execute(db.select(Car))
    cars = result.scalars().all()
    all_categories = CarCategoryEnum.__members__
    category_requested = request.args.get("category")
    if category_requested in all_categories:
        category_requested = all_categories[category_requested].name
        cars = [car for car in cars if car.category.name == category_requested]
    else:
        category_requested = None
    return render_template("cars.html", active_page='cars', cars=cars, categories=all_categories, choice=category_requested)


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


@app.route("/add_car/", methods=["GET", "POST"])
@login_required
def add_car():
    form = CarForm()
    if form.validate_on_submit():
        new_car = Car()
        form.populate_obj(new_car)
        db.session.add(new_car)
        try:
            db.session.commit()
            flash('Авто успішно додано!', 'success')
            return redirect(url_for('all_cars'))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('Авто з такою назвою вже є у базі даних!', 'danger')
    return render_template("add_car.html", form=form)


@app.route("/edit_car/<int:car_id>", methods=["GET", "POST"])
@login_required
def edit_car(car_id):
    car = db.get_or_404(Car, car_id)
    form = CarForm(obj=car)
    if form.validate_on_submit():
        form.populate_obj(car)
        try:
            db.session.commit()
            flash('Інформацію про авто успішно змінено!', 'success')
            return redirect(url_for('all_cars'))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('Авто з такою назвою вже є у базі даних! Зміни не було збережено!', 'danger')
    return render_template("add_car.html", form=form, is_edit=True)


@app.route("/delete_car/<int:car_id>")
@login_required
def delete_car(car_id):
    car = db.get_or_404(Car, car_id)
    db.session.delete(car)
    try:
        db.session.commit()
        flash('Авто успішно видалено!', 'success')
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        flash('Неможливо видалити, оскільки у базі даних є бронювання на дане авто!', 'danger')
    return redirect(url_for('all_cars'))


if __name__ == "__main__":
    app.run(debug=True)
