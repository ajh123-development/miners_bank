from flask import Flask
from flask_login import LoginManager
from sqlalchemy import select
from miners_bank.database import db_session, init_db, serialize
from miners_bank.routes.auth import auth_blueprint
from miners_bank.routes.main import main_blueprint
from miners_bank.routes.bank import bank_blueprint
from miners_bank.models.account import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
init_db()

app.register_blueprint(auth_blueprint)
app.register_blueprint(bank_blueprint)
app.register_blueprint(main_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    stmt = select(User).where(User.user_id.in_([user_id]))
    user = db_session.scalars(stmt).first()
    return user

if __name__ == "__main__":
    app.run()
