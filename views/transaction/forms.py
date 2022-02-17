from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import ValidationError
from wtforms.fields import IntegerField, SelectField, SubmitField
from .transactions_func import check_if_account_exist 

def check_valid_account_id(form, field):
    if not check_if_account_exist(field.data):
        raise ValidationError('Account id does not exist!')

def check_valid_transactions_option(form, field):
    if not field.data:
        raise ValidationError('Select operation!')

def check_sufficient_balance(form, field):
    pass

class TransactionsDeposit(FlaskForm):
    account_id = IntegerField("account_id",
    [validators.NumberRange(min=1, message='Not a valid account ID!'), check_valid_account_id])

    amount = IntegerField("amount", [validators.NumberRange(min=1)])

    operation = SelectField("operation", [check_valid_transactions_option],
    choices= [("0",""),("1","Deposit cash"),("2","Salary"),("3","Transfer")],coerce=int)
    
    submit = SubmitField("Submit")
