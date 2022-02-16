from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import false
from models import Account, Transaction


accounts = Blueprint('accounts',__name__, template_folder='templates')

def transaction_serialize(tr:Transaction) -> dict:
    return {"Id" : tr.Id, "Type":tr.Type, "Date":tr.Date.strftime("%Y-%m-%d %H:%M:%S"), "Amount":tr.Amount, "NewBalance":tr.NewBalance}

@accounts.route("/<id>")
def account_page(id):
    account = Account.query.where(Account.Id == id).first()
    transactions = Transaction.query.where(Transaction.AccountId == id).order_by(Transaction.Date.desc()).paginate(1,5,False)
    return render_template("accounts/accountPage.html", account=account, transactions=transactions, page=1)

@accounts.route("/api/<id>/transactions")
def account_transactions(id):
    page = request.args.get("page",2, type=int)
    pag_object = Transaction.query.where(Transaction.AccountId == id).order_by(Transaction.Date.desc()).paginate(page,5,False)
    return jsonify([transaction_serialize(transaction) for transaction in pag_object.items])