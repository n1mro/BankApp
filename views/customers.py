from ast import Raise
from logging import exception
from flask import Blueprint, render_template, request
from models import Customer
from enum import Enum


customers = Blueprint('customers',__name__, template_folder='templates')

class SortOrder(Enum):
    asc = "asc"
    desc = "desc"

class CustomerColumn(Enum):
    Id = "Id"
    NationalId = "NationalId"
    GivenName = "GivenName"
    Streetaddress = "Streetaddress"
    Country = "Country"

def sort_order_func(sort_order:SortOrder, column:CustomerColumn):
    column_to_be_sorted = select_customer_column(column)
    return column_to_be_sorted.desc if sort_order==SortOrder.desc else column_to_be_sorted.asc

def select_customer_column(column:CustomerColumn):
    if column == CustomerColumn.Id:
        return Customer.Id
    elif column == CustomerColumn.NationalId:
        return Customer.NationalId
    elif column == CustomerColumn.GivenName:
        return Customer.GivenName
    elif column == CustomerColumn.Streetaddress:
        return Customer.Streetaddress
    elif column == CustomerColumn.Country:
        return Customer.Country
    else:
        #Kontrollera detta!!!
        Raise(exception("Not implemented",ValueError))
    

@customers.route("/list")
def table_of_customers():
    sort_order = request.args.get('sort_order', 'asc')
    sort_column = request.args.get('sort_column', 'Id')
    q = request.args.get('q','')

    page = int(request.args.get('page',1))

    table_of_customer = Customer.query.filter(
        Customer.Id.like(f"%{q}%") |
        Customer.NationalId.like(f"%{q}%") |
        Customer.GivenName.like(f"%{q}%") |
        Customer.Streetaddress.like(f"%{q}%") |
        Customer.Country.like(f"%{q}%") 
    )

    sort_by = sort_order_func(SortOrder(sort_order),CustomerColumn(sort_column))

    table_of_customer = table_of_customer.order_by(sort_by())
    pagination_object = table_of_customer.paginate(page,20,False)
    
    return render_template('customers/listCustomers.html',
            page=page,
            sort_order=sort_order,
            sort_column=sort_column,
            q=q,
            pagination=pagination_object)


@customers.route("/<id>")
def customer_page(id):
    customer = Customer.query.where(Customer.Id==id).first()
    return render_template('customers/customerPage.html', customer=customer)
    