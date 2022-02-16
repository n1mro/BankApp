from flask import Blueprint, render_template, request
from models import Account, Customer
from .customers_func import sort_order_func,SortOrderEnum,CustomerColumnEnum


customers = Blueprint('customers',__name__, template_folder='templates')


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

    sort_by = sort_order_func(SortOrderEnum(sort_order),CustomerColumnEnum(sort_by_column))

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
    

