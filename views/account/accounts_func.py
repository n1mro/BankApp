from models import Transaction


def transaction_serialize(tr:Transaction) -> dict:
    return {"Id" : tr.Id, 
            "Type":tr.Type,
            "Date":tr.Date.strftime("%Y-%m-%d %H:%M:%S"), 
            "Amount":tr.Amount, 
            "NewBalance":tr.NewBalance,
            "Operation":tr.Operation
            }