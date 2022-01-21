from flask import Blueprint, render_template, request
from models import Customer
from enum import Enum


customers = Blueprint('customers',__name__, template_folder='templates')

class SortOrder(Enum):
    asc = "asc"
    desc = "desc"

class ColumnToBeSorted(Enum):
    Id = 'id'
    NationalId = 'national_id'
    GivenName = 'given_name'
    Streetaddress = 'streetaddress'
    Country = 'country'

@customers.route("/list")
def table_of_customers():
    sort_order = SortOrder(request.args.get('sort_order', 'asc'))
    sort_column = ColumnToBeSorted(request.args.get('sort_column', 'id'))
    
    return render_template('customers/listCustomers.html', customer_list = Customer.query.limit(100))