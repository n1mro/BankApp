from flask import Blueprint, render_template, request
from models import Account
from .transactions_enum import TransactionsTypeEnum
from .forms import TransactionsDeposit, TransactionCredit
from .transactions_func import make_transaction, update_account_balance

transactions = Blueprint('transactions',__name__)

@transactions.route("/successful")
def transaction_successful():
    return render_template("'transaction/successful.html")

@transactions.route("/deposit", methods=["GET", "POST"])
def deposit_transaction():
    form  = TransactionsDeposit()
    if request.method == "GET":
        return render_template('transactions/deposit.html', form=form)

    if form.validate_on_submit():
        acc = Account.query.where(Account.Id == form.account_id.data).first()
        make_transaction(form,acc,TransactionsTypeEnum(1))
        update_account_balance(form.amount.data,acc,TransactionsTypeEnum(1))
        return render_template('transactions/transaction_successful.html', acc_id=acc.Id, balance=acc.Balance)

    return render_template('transactions/deposit.html', form=form)


@transactions.route("/credit", methods=["GET", "POST"])
def credit_transaction():
    form = TransactionCredit()
    if request.method == "GET":
        return render_template('transactions/credit.html', form=form)

    if form.validate_on_submit():
        acc = Account.query.where(Account.Id == form.account_id.data).first()
        make_transaction(form,acc,TransactionsTypeEnum(2))
        update_account_balance(form.amount.data,acc,TransactionsTypeEnum(2))
        return render_template('transactions/transaction_successful.html', acc_id=acc.Id, balance=acc.Balance)

    return render_template('transactions/credit.html', form=form)