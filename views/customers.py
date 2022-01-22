from ast import Raise
from logging import exception
from flask import Blueprint, render_template, request
from sqlalchemy import asc,desc
from models import Customer
from enum import Enum


customers = Blueprint('customers',__name__, template_folder='templates')

class SortOrder(Enum):
    asc = "asc"
    desc = "desc"

class ColumnToBeSorted(Enum):
    Id = "Id"
    NationalId = "NationalId"
    GivenName = "GivenName"
    Streetaddress = "Streetaddress"
    Country = "Country"

def sort_order_func(sort_order:SortOrder, column:ColumnToBeSorted):
    column_to_be_sorted = select_column(column)
    return column_to_be_sorted.desc if sort_order==SortOrder.desc else column_to_be_sorted.asc

def select_column(column:ColumnToBeSorted):
    if column == ColumnToBeSorted.Id:
        return Customer.Id
    elif column == ColumnToBeSorted.NationalId:
        return Customer.NationalId
    elif column == ColumnToBeSorted.GivenName:
        return Customer.GivenName
    elif column == ColumnToBeSorted.Streetaddress:
        return Customer.Streetaddress
    elif column == ColumnToBeSorted.Country:
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
    active_page="table_of_customers"

    table_of_customer = Customer.query.filter(
        Customer.Id.like(f"%{q}%") |
        Customer.NationalId.like(f"%{q}%") |
        Customer.GivenName.like(f"%{q}%") |
        Customer.Streetaddress.like(f"%{q}%") |
        Customer.Country.like(f"%{q}%") 
    )

    sort_by = sort_order_func(SortOrder(sort_order),ColumnToBeSorted(sort_column))

    table_of_customer = table_of_customer.order_by(sort_by())
    pagination_object = table_of_customer.paginate(page,20,False)
    
    return render_template('customers/listCustomers.html', 
            customer_list = pagination_object.items,
            page=page,
            sort_order=sort_order,
            sort_column=sort_column,
            q=q,
            has_next = pagination_object.has_next,
            has_prev=pagination_object.has_prev,
            pages=pagination_object.pages,
            active_page=active_page)