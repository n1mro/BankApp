from enum import Enum

class TransactionsTypeEnum(Enum):
    Debit = 1
    Credit = 2

class TransactionsOperationsEnum(Enum):
    Deposit_cash = 1
    Salary = 2
    Transfer = 3
    ATM_withdrawal = 4
    Payment = 5
    Bank_withdrawal = 6