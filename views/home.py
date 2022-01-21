from flask import Blueprint, render_template
from models import Customer, Account, db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


home = Blueprint('home',__name__, template_folder='templates')

@home.route('/')
@home.route('/home')
def index():
    index_body_parameters = {
    "number_of_customers": Customer.query.count(),
    "number_of_accounts": Account.query.count(),
    "total_amount_in_accounts": db.session.query(func.sum(Account.Balance)).scalar()
    }
    return render_template('home/index.html', **index_body_parameters)
