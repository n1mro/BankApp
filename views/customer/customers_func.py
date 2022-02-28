from enum import Enum
from models import Customer

class ColumnError(Exception):
    def __init__(self, message:str = "Not implemented or not a valid CustomerColumn variable!") -> None:
        self.message = message
        super().__init__(self.message)

class SortOrderEnum(Enum):
    asc = "asc"
    desc = "desc"

class CustomerColumnEnum(Enum):
    Id = "Id"
    NationalId = "NationalId"
    GivenName = "GivenName"
    Streetaddress = "Streetaddress"
    Country = "Country"

def sort_order_func(sort_order:SortOrderEnum, column:CustomerColumnEnum):
    """Retruns a callable Customer colum sort order function"""
    column_to_be_sorted = select_customer_column(column)
    return column_to_be_sorted.desc if sort_order==SortOrderEnum.desc else column_to_be_sorted.asc

def select_customer_column(column:CustomerColumnEnum):
    """Returns a Customer colum"""
    if column == CustomerColumnEnum.Id:
        return Customer.Id
    elif column == CustomerColumnEnum.NationalId:
        return Customer.NationalId
    elif column == CustomerColumnEnum.GivenName:
        return Customer.GivenName
    elif column == CustomerColumnEnum.Streetaddress:
        return Customer.Streetaddress
    elif column == CustomerColumnEnum.Country:
        return Customer.Country
    else:
        raise ColumnError
 

def check_if_valid_customer_id(id:int) -> bool:
    return True if Customer.query.where(Customer.Id == id).first() else False