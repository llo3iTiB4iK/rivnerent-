from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.context_processor
def inject_stage_and_region():
    return {'ADMIN_PHONE_NUM': os.environ.get("ADMIN_PHONE")}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cars/")
def all_cars():
    return render_template("cars.html")


@app.route("/rules/")
def rules_n_terms():
    return render_template("rules.html")


@app.route("/about/")
def about_us():
    return render_template("about_us.html")


@app.route("/login/")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
