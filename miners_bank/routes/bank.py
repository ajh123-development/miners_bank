from flask import Blueprint
from ..database import db_session


bank_blueprint = Blueprint('bank', __name__)
