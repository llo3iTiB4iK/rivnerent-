from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, URLField, TextAreaField, FloatField, IntegerField
from wtforms.validators import DataRequired, URL, NumberRange
from .models import CarCategoryEnum, FuelTypeEnum, TransmissionEnum


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
    category = SelectField('Категорія', validators=[MyDataRequired()], choices=[(member.name, member.value) for member in CarCategoryEnum])
    img_url = URLField('Посилання на зображення', validators=[MyDataRequired(), MyURL()],
                       render_kw={"placeholder": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Audi_A6_Allroad_Quattro_C8_1X7A0301.jpg"})
    description = TextAreaField('Опис', validators=[MyDataRequired()], render_kw={"placeholder": "Надійний, елегантний універсал для подорожей з сім'єю."})
    engine_size = FloatField('Об\'єм двигуна (л)', validators=[MyDataRequired("Об'єм двигуна має бути задано у форматі числа з плаваючою крапкою"),
                                                               NumberRange(0, message="Літраж двигуна повинен перевищувати 0")], render_kw={"placeholder": "2.0"})
    fuel_type = SelectField('Тип пального', validators=[MyDataRequired()], choices=[(member.name, member.value) for member in FuelTypeEnum])
    transmission = SelectField('Тип КПП', validators=[MyDataRequired()], choices=[(member.name, member.value) for member in TransmissionEnum])
    seats = IntegerField('Кількість місць', validators=[MyDataRequired(), NumberRange(1, message="Авто повинне мати хоча б 1 місце")], render_kw={"placeholder": "5"})
    info_url = URLField('Посилання на детальні характеристики авто', validators=[MyDataRequired(), MyURL()],
                       render_kw={"placeholder": "https://audi-a6-allroad-quattro.infocar.ua/mod_14642_a6-allroad-quattro_id5893.html"})
    price_1to3 = StringField('Вартість за добу (термін прокату 1-3 діб)', validators=[MyDataRequired()], render_kw={"placeholder": "999 $"})
    price_4to9 = StringField('Вартість за добу (термін прокату 4-9 діб)', validators=[MyDataRequired()], render_kw={"placeholder": "999 $"})
    price_10to25 = StringField('Вартість за добу (термін прокату 10-25 діб)', validators=[MyDataRequired()], render_kw={"placeholder": "999 $"})
    price_26to89 = StringField('Вартість за добу (термін прокату 26-89 діб)', validators=[MyDataRequired()], render_kw={"placeholder": "999 $"})
    deposit = StringField('Розмір завдатку', validators=[MyDataRequired()], render_kw={"placeholder": "999 $"})
    submit = SubmitField('Зберегти')
