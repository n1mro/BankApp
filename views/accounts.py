from flask import Blueprint, render_template, request
from models import Account, Transaction


accounts = Blueprint('accounts',__name__, template_folder='templates')


@accounts.route("/<id>")
def account_page(id):
    account = Account.query.where(Account.Id == id).first()
    transactions = Transaction.query.where(Transaction.AccountId == id).order_by(Transaction.Date.desc())
    return render_template("accounts/accountPage.html", account=account, transactions=transactions)

