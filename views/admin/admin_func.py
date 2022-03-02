from dataclasses import FrozenInstanceError
from models import User, user_manager
from .admin_enum import RoleType

def check_if_User_email_exist_in_database(email:str) -> bool:
    return True if User.query.where(User.email == email).first() else False

def get_role_type(type:RoleType):
    if type == RoleType.Admin:
        return "Admin"
    elif type == RoleType.Cashier:
        return "Cashier"
    else:
        raise ValueError("Not implemented Roletype in get_role_type!")

def fetch_user_from_database_by_user_id(user_id:int) -> User:
    return User.query.where(User.id == user_id).first()

def check_if_user_id_exist(user_id:int) -> bool:
    return True if fetch_user_from_database_by_user_id(user_id) else False

def check_if_password_is_correct_for_user_id(pwd:str, user_id:int) -> bool:
    user = fetch_user_from_database_by_user_id(user_id)
    return user_manager.verify_password(pwd,user.password)

def check_that_user_id_has_email_or_email_is_not_used( email:str, user_id:int) -> bool:
    user = fetch_user_from_database_by_user_id(user_id)

    if user.email == email:
        return True
    else:
        return not check_if_User_email_exist_in_database(email)

    
