from flask import Blueprint, render_template, request
from models import Account


accounts = Blueprint('accounts',__name__, template_folder='templates')


@accounts.route("/<id>")
def account_page(id):
    account = Account.query.where(Account.Id == id).first()
    return render_template("accounts/accountPage.html", account=account)