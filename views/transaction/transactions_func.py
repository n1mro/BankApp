from models import Account, Transaction, db
from .transactions_enum import TransactionsTypeEnum,TransactionsOperationsEnum
from datetime import datetime

def get_transaction_operation(operation:TransactionsOperationsEnum)->str:
    if operation==TransactionsOperationsEnum.Deposit_cash:
        return "Deposit cash"
    elif operation==TransactionsOperationsEnum.Salary:
        return "Salary"
    elif operation==TransactionsOperationsEnum.Transfer:
        return "Transfer"
    elif operation==TransactionsOperationsEnum.Payment:
        return "Payment"
    elif operation==TransactionsOperationsEnum.ATM_withdrawal:
        return "ATM withdrawl"
    elif operation==TransactionsOperationsEnum.Bank_withdrawal:
        return "Bank withdrawl"
    else:
        raise ValueError("Not implimented get_transaction_operation")

def get_transaction_type(type:TransactionsTypeEnum) -> str:
    if type==TransactionsTypeEnum.Debit:
        return "Debit"
    elif type==TransactionsTypeEnum.Credit:
        return "Credit"
    else:
        raise ValueError("Not implemented get_transaction_type")

def check_if_account_exist(id:int) -> bool:
    return True if Account.query.where(Account.Id == id).first() else False

def check_if_amount_less_than_or_equal_account_balance(id:int,amount:int) -> bool:
    if (acc:=Account.query.where(Account.Id == id).first()):
        return True if amount<=acc.Balance else False
    else:
        raise ValueError("Not a valid account id!!!")

def update_account_balance(amount:int, acc:Account,type:TransactionsTypeEnum) -> None:
    if type==TransactionsTypeEnum.Debit:
        acc.Balance += amount
        db.session.add(acc)
        db.session.commit()
    elif type==TransactionsTypeEnum.Credit:
        acc.Balance -= amount
        db.session.add(acc)
        db.session.commit()
    else:
        raise ValueError("Not implemented TransactionsTypeEnum in update_account_balance!")

def make_transaction(operation:int,amount:int, acc:Account, type_of_transaction:TransactionsTypeEnum) -> None:
    transaction_to_be_made = Transaction()
    
    transaction_to_be_made.AccountId = acc.Id
    transaction_to_be_made.Date = datetime.now()
    transaction_to_be_made.Amount = amount

    transaction_to_be_made.Type = get_transaction_type(type_of_transaction)

    transaction_to_be_made.Operation = get_transaction_operation(TransactionsOperationsEnum(operation))

    transaction_to_be_made.NewBalance = (
        acc.Balance + amount) if (type_of_transaction == TransactionsTypeEnum.Debit) else (acc.Balance - amount)

    db.session.add(transaction_to_be_made)
    db.session.commit()

    update_account_balance(amount,acc,type_of_transaction)
