from flask import Blueprint, render_template
from models import Customer


listCostumers = Blueprint('listCostumers',__name__, template_folder='templates')


@listCostumers.route("/list")
def table():
    return render_template('customers/tabledataBasetemplate.html', customer_list = Customer.query.limit(100))