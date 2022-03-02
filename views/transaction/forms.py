from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import ValidationError
from wtforms.fields import IntegerField, SelectField, SubmitField
from .transactions_func import check_if_account_exist, check_if_amount_less_than_or_equal_account_balance

def check_valid_account_id(form, field):
    if not check_if_account_exist(field.data):
        raise ValidationError('Account id does not exist!')

def check_valid_SelectField_option(form, field):
    if not field.data:
        raise ValidationError('Select operation!')

def check_sufficient_balance(form, field):
    if not check_if_amount_less_than_or_equal_account_balance(form.account_id.data,field.data):
        raise ValidationError('Insufficient funds on account!!!')

class TransactionsDeposit(FlaskForm):
    account_id = IntegerField(
        "Account ID",
        [validators.NumberRange(min=1, message='Not a valid account ID!'), check_valid_account_id]
        )

    amount = IntegerField("Amount", [validators.NumberRange(min=1)])

    operation = SelectField(
        "Operation", 
        [check_valid_SelectField_option],
        choices= [("0",""),("1","Deposit cash"),("2","Salary"),("3","Transfer")],
        coerce=int
        )
    
    submit_deposit = SubmitField("Submit")

class TransactionCredit(FlaskForm):
    account_id = IntegerField(
        "Account ID",
        [validators.NumberRange(min=1, message='Not a valid account ID!'), check_valid_account_id]
        )

    amount = IntegerField("Amount", [validators.NumberRange(min=1),check_sufficient_balance])

    operation = SelectField(
        "Operation", 
        [check_valid_SelectField_option],
        choices= [("0",""),("4","ATM withdrawal"),("5","Payment"),("6","Bank withdrawal"),("3","Transfer")],
        coerce=int
        )
    
    submit_credit = SubmitField("Submit")

class TransferWithinBank(FlaskForm):
    
    account_id = IntegerField(
        "Withdraw from Account",
        [validators.NumberRange(min=1, message='Not a valid account ID!'), check_valid_account_id]
        )

    account_id_debit = IntegerField(
        "Transfer to Account",
        [validators.NumberRange(min=1, message='Not a valid account ID!'), check_valid_account_id]
        )

    amount = IntegerField("Amount", [validators.NumberRange(min=1),check_sufficient_balance])

    submit_transfer = SubmitField("Submit")