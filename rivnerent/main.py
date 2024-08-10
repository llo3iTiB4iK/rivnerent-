from flask import Blueprint, render_template, request
from .models import Car, CarCategoryEnum, AdditionalService
from .extensions import db

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
def home():
    return render_template("index.html", active_page='home')


@main_bp.route("/cars/")
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
    result = db.session.execute(db.select(AdditionalService))
    services = result.scalars().all()
    return render_template("cars.html", active_page='cars', cars=cars, categories=all_categories, choice=category_requested, services=services)


@main_bp.route("/cars/<car_name>")
def show_car(car_name):
    try:
        car_id = int(car_name.split('_id')[-1])
    except ValueError:
        car_id = None
    car = db.get_or_404(Car, car_id)
    return render_template("car.html", active_page='cars', car=car)


@main_bp.route("/booking/")
def book_car():
    car_id = request.args.get("car")
    car = db.get_or_404(Car, car_id)
    return render_template("booking.html", car=car)


@main_bp.route("/rules/")
def rules_n_terms():
    return render_template("rules.html", active_page='rules')


@main_bp.route("/about/")
def about_us():
    return render_template("about_us.html", active_page='about')
