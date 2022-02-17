from enum import Enum

class TransactionsType(Enum):
    Debit = 1
    Credit = 2

class TransactionsOperationsEnum(Enum):
    Deposit_cash = 1
    Salary = 2
    Transfer = 3