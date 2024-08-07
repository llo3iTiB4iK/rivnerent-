import sqlalchemy.exc
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from .forms import CarForm
from .models import Car
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
