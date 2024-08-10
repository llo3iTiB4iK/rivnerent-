import sqlalchemy.exc
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from .forms import CarForm
from .models import Car, AdditionalService
from .extensions import db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route("/add_car/", methods=["GET", "POST"])
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
            return redirect(url_for('main.all_cars'))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('Авто з такою назвою вже є у базі даних!', 'danger')
    return render_template("add_car.html", form=form)


@admin_bp.route("/edit_car/<int:car_id>", methods=["GET", "POST"])
@login_required
def edit_car(car_id):
    car = db.get_or_404(Car, car_id)
    form = CarForm(obj=car)
    form.category.data = car.category.name
    form.fuel_type.data = car.fuel_type.name
    form.transmission.data = car.transmission.name
    if form.validate_on_submit():
        form.populate_obj(car)
        try:
            db.session.commit()
            flash('Інформацію про авто успішно змінено!', 'success')
            return redirect(url_for('main.all_cars'))
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            flash('Авто з такою назвою вже є у базі даних! Зміни не було збережено!', 'danger')
    return render_template("add_car.html", form=form, is_edit=True)


@admin_bp.route("/delete_car/<int:car_id>")
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
    return redirect(url_for('main.all_cars'))


@admin_bp.route("/add_service/", methods=["POST"])
@login_required
def add_service():
    form = request.form
    new_service = AdditionalService(name=form.get("name"), daily_price=form.get("daily_price"), max_price=form.get("max_price"))
    db.session.add(new_service)
    try:
        db.session.commit()
        flash('Додаткову послугу успішно додано!', 'success')
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        flash('Не вдалося додати додаткову послугу! Можливо, послуга з такою назвою вже є в базі даних.', 'danger')
    return redirect(url_for("main.all_cars"))


@admin_bp.route("/delete_service/<int:service_id>")
@login_required
def delete_service(service_id):
    service = db.get_or_404(AdditionalService, service_id)
    db.session.delete(service)
    try:
        db.session.commit()
        flash('Додаткову послугу успішно видалено!', 'success')
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        flash('Неможливо видалити, оскільки у базі даних є бронювання з вибором даної послуги!', 'danger')
    return redirect(url_for('main.all_cars'))
