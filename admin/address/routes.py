from main import app
from flask import Blueprint


blueprint = Blueprint('address', __name__)

@blueprint.route('/home/')
def home():
    return "home"