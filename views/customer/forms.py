from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import ValidationError
from wtforms.fields import IntegerField, SubmitField
from .customers_func import check_if_valid_customer_id

def check_valid_customer_id(form, field):
    if not check_if_valid_customer_id(field.data):
        raise ValidationError('Customer id does not exist!')

class CustomerID(FlaskForm):
    customer_id = IntegerField("customer_id",
        [validators.NumberRange(min=1, message='Not a valid customer ID!'), check_valid_customer_id])

    submit_customer_id = SubmitField("Submit")