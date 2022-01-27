from flask import Blueprint, render_template, request
from models import Account, Customer
from enum import Enum


customers = Blueprint('customers',__name__, template_folder='templates')


class ColumnError(Exception):
    def __init__(self, message:str = "Not implemented or not a valid CustomerColumn variable!") -> None:
        self.message = message
        super().__init__(self.message)

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
    """Retruns a callable Customer colum sort order function"""
    column_to_be_sorted = select_customer_column(column)
    return column_to_be_sorted.desc if sort_order==SortOrder.desc else column_to_be_sorted.asc

def select_customer_column(column:CustomerColumn):
    """Returns a Customer colum"""
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
        raise ColumnError
    

@customers.route("/list")
def table_of_customers():
    sort_order = request.args.get('sort_order', 'asc')
    sort_by_column = request.args.get('sort_column', 'Id')
    q = request.args.get('q','')

    page = request.args.get('page',1,type=int)

    table_of_customer = Customer.query.filter(
        Customer.Id.like(f"%{q}%") |
        Customer.NationalId.like(f"%{q}%") |
        Customer.GivenName.like(f"%{q}%") |
        Customer.Streetaddress.like(f"%{q}%") |
        Customer.Country.like(f"%{q}%") 
    )

    sort_by = sort_order_func(SortOrder(sort_order),CustomerColumn(sort_by_column))

    table_of_customer = table_of_customer.order_by(sort_by())
    pagination_object = table_of_customer.paginate(page,20,False)
    
    return render_template('customers/listCustomers.html',
            page=page,
            sort_order=sort_order,
            sort_column=sort_by_column,
            q=q,
            pagination=pagination_object)


@customers.route("/<id>")
def customer_page(id):
    customer = Customer.query.where(Customer.Id==id).first()
    customer_accounts = Account.query.where(Account.CustomerId == id).all()
    sum_of_accounts_balance = sum([customer.Balance for customer in customer_accounts])

    return render_template('customers/customerPage.html',
             customer=customer,
             accounts=customer_accounts,
             account_balance_sum = sum_of_accounts_balance)
    

