from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import ValidationError
from wtforms.fields import SelectField, SubmitField, StringField, BooleanField, PasswordField, IntegerField
from .admin_func import check_if_User_email_exist_in_database,check_if_user_id_exist\
    ,check_if_password_is_correct_for_user_id,check_that_user_id_has_email_or_email_is_not_used

def check_valid_SelectField_option(form, field):
    if not field.data:
        raise ValidationError('Select operation!')

def check_if_email_is_a_valid_and_not_used(form, field):
    if check_if_User_email_exist_in_database(field.data):
        raise ValidationError('Email already exist!')

def check_if_valid_user_id(form,field):
    if not check_if_user_id_exist(field.data):
        raise ValidationError('User-id does not exist!')

def check_if_valid_old_user_password(form,field):
    if not check_if_password_is_correct_for_user_id(field.data, form.user_id.data):
        raise ValidationError('Incorrect entered password!!!')

def check_if_valid_email_addres_change(form,field):
    if not check_that_user_id_has_email_or_email_is_not_used(field.data, form.user_id.data):
        raise ValidationError('Email already exist!!!')

class UserFormBasic(FlaskForm):

    first_name = StringField("First Name",[validators.Length(min=2,max=30,message="Between 2 and 30 characters")])
    last_name = StringField("Last Name",[validators.Length(min=2,max=30,message="Between 2 and 30 characters")])

    email = StringField("Email",[validators.email(),check_if_email_is_a_valid_and_not_used])

    active = BooleanField("Active User", default="checked")

    password = PasswordField(
        "Password",
        [validators.Length(min=8,max=64,message="Between 8 and 64 characters"),
        validators.EqualTo("password_confirm",message="Missmatch in confirmed password")]
        )

    password_confirm = PasswordField(
        "Confirm Password",
        [validators.Length(min=8,max=64,message="Between 8 and 64 characters")]
        )

    roles = SelectField(
        "Roles", 
        [check_valid_SelectField_option],
        choices= [("0",""),("1","Admin"),("2","Cashier")],
        coerce=int
        )
    

class UserFormCreate(UserFormBasic):
    submit_user_create = SubmitField("Create")

class UserFormGetUserID(FlaskForm):
    user_id = IntegerField("User ID",[validators.NumberRange(min=1),check_if_valid_user_id])

class UserFormDelete(UserFormGetUserID):
    submit_user_delete = SubmitField("Delete")


class UserFormUpdateChoice(UserFormGetUserID):
    submit_user_update_password = SubmitField("Update Password")
    submit_user_update_credentials = SubmitField("Update Credentials")
    submit_user_update_roles = SubmitField("Update Role")
    submit_user_update_activity = SubmitField("Update Activity")


class UserFormUpdatePassword(UserFormGetUserID):
    old_password=PasswordField(
        "Old Password",
        [validators.Length(min=8,max=64,message="Between 8 and 64 characters"),check_if_valid_old_user_password]
        )

    new_password = PasswordField(
        "Password",
        [validators.Length(min=8,max=64,message="Between 8 and 64 characters"),
        validators.EqualTo("new_password_confirm",message="Missmatch in confirmed password")]
        )

    new_password_confirm = PasswordField(
        "Confirm Password",
        [validators.Length(min=8,max=64,message="Between 8 and 64 characters")]
        )

    submit_new_password = SubmitField("Submit")

class UserFormUpdateCredentials( UserFormGetUserID ):
    first_name = StringField("First Name",[validators.Length(min=2,max=30,message="Between 2 and 30 characters")])
    last_name = StringField("Last Name",[validators.Length(min=2,max=30,message="Between 2 and 30 characters")])

    email = StringField("Email",[validators.email(),check_if_valid_email_addres_change])

    submit_new_credentials = SubmitField("Submit")


