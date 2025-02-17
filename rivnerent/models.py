from flask_login import UserMixin
from sqlalchemy import Integer, String, Enum, Text, Float, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
import enum
from .extensions import db


# Клас користувача для Flask-Login
class User(UserMixin):
    def __init__(self, id_):
        self.id = id_


# Клас авто та використовувані ним перелічувані типи
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

    def get_price_for_period(self, days):
        if 1 <= days <= 3:
            return days * int(self.price_1to3.replace(" ₴", ""))
        elif 4 <= days <= 9:
            return days * int(self.price_4to9.replace(" ₴", ""))
        elif 10 <= days <= 25:
            return days * int(self.price_10to25.replace(" ₴", ""))
        elif 26 <= days <= 89:
            return days * int(self.price_26to89.replace(" ₴", ""))
        else:
            raise ValueError


class AdditionalService(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    daily_price: Mapped[str] = mapped_column(String(20), nullable=False)
    max_price: Mapped[str] = mapped_column(String(20), nullable=False)

    def get_price_for_period(self, days):
        return min(int(self.daily_price.replace(" ₴", "")) * days, int(self.max_price.replace(" ₴", "")))
