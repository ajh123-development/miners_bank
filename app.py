import os
import bcrypt
from miners_bank import account
from miners_bank import atm
from miners_bank import bank
from miners_bank import currencey
from miners_bank import Base
from miners_bank.database import db_session, init_db, serialize

from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_login import login_required
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

#bob = account.Account (pin_code = 1066,currencey = currencey.Currencey (value = 100,currencey_type = currencey.CurrenceyType(name = "Samland Dollar",symbol = "$",shortName = "SLD")),user = account.User (name = "Bob"),bank = bank.Bank (name = "Bank of Samland"))
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    return ""

@app.route('/banks/all')
@login_required
def all_banks():
    banks = db_session.query(bank.Bank).all()
    new_banks = []
    for loop_bank in banks:
        new_banks.append(serialize(loop_bank))
    return jsonify(new_banks)

@app.route('/banks/create', methods=('GET', 'POST'))
@login_required
def create_bank():
    if request.method == 'POST':
        name = request.form['name']
        new_bank = bank.Bank(name=name)
        db_session.add(new_bank)
        db_session.commit()

        return redirect(url_for('index'))
    return render_template('bank_create.html')


@bull.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. 
    For POSTS, login the current user by processing the form.

    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        if user:
            if bcrypt.checkpw(form.password.data, user.password):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("bull.reports"))
    return render_template("login.html", form=form)

@bull.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")

if __name__ == "__main__":
    app.run()
