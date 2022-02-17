from models import Account, Transaction, db
from .transactions_enum import TransactionsType,TransactionsOperationsEnum
from datetime import datetime

def get_transaction_operation(operation:TransactionsOperationsEnum)->str:
    if operation==TransactionsOperationsEnum.Deposit_cash:
        return "Deposit cash"
    elif operation==TransactionsOperationsEnum.Salary:
        return "Salary"
    elif operation==TransactionsOperationsEnum.Transfer:
        return "Transfer"
    else:
        pass

def check_if_account_exist(id:int) -> bool:
    return True if Account.query.where(Account.Id == id).first() else False

def update_account_balance(amount:int, acc:Account,type:TransactionsType) -> None:
    if type.Debit:
        acc.Balance += amount
        db.session.add(acc)
        db.session.commit()
    elif type.Credit:
        acc.Balance -= amount
        db.session.add(acc)
        db.session.commit()
    else:
        raise ValueError

def make_transaction(form, acc:Account) -> None:
    transaction_to_be_made = Transaction()
    transaction_to_be_made.AccountId = acc.Id
    transaction_to_be_made.Date = datetime.now()
    transaction_to_be_made.Amount = form.amount.data
    transaction_to_be_made.Type = "Debit"
    transaction_to_be_made.Operation = get_transaction_operation(TransactionsOperationsEnum(form.operation.data))
    transaction_to_be_made.NewBalance = acc.Balance + form.amount.data
    db.session.add(transaction_to_be_made)
    db.session.commit()
