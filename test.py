import unittest
from app import app
from models import Account,Transaction
from random import randint



class TransactionsTestCases(unittest.TestCase):
    """Assumes that there is at least 2 accounts, Id:1,2 are in the database. Also no that transactions have been deleted
       so that there are no holes in the transactionshistory on Transaction.Id"""


    def setUp(self):
        app.config.from_object('config.ConfigTest')
        app.config['LOGIN_DISABLED']=True
        self.ctx = app.app_context()
        self.ctx.push()

    def test_1_if_main_page_is_accessible(self):
        test_client = app.test_client()
        with test_client as c:
            respons = c.get("/home")
            self.assertEqual(respons.status_code , 200)

    def test_2_required_login_when_LOGIN_DISABLE_set_to_False(self):
        test_client = app.test_client()
        with test_client as c:
            app.config['LOGIN_DISABLED']=False
            respons = c.get("/customer/list")
            #app.config['LOGIN_DISABLED']=True
            self.assertEqual(respons.status_code , 302)
    
    def test_3_required_login_when_LOGIN_DISABLE_if_global_set_to_True(self):
        test_client = app.test_client()
        with test_client as c:
            respons = c.get("/customer/list")
            self.assertEqual(respons.status_code, 200)

    def test_4_to_deposit_valid_input(self):
        test_client = app.test_client()
        with test_client as c:
            random_amount = randint(10,100)
            account_1 = Account.query.where(Account.Id == 1).first()
            starting_balance = account_1.Balance
            ending_balance = starting_balance + random_amount

            respons = c.post(
                '/transactions/deposit', 
                data = {'account_id':'1', 'amount':f'{random_amount}','operation':"1"})
            self.assertEqual(respons.status_code , 302)

            # Check that accounts is updated
            self.assertEqual(
                ending_balance,
                Account.query.where(Account.Id == 1).first().Balance
                )

            # Check that a correct transaction has happend
            # Assumpion that no transactions is ever deleted
            latest_transaction_for_account_1 = Transaction.query.where(
                                            Transaction.AccountId == 1).order_by(
                                            Transaction.Id.desc()).first()
            self.assertEqual(latest_transaction_for_account_1.Amount , random_amount)
            self.assertEqual(latest_transaction_for_account_1.NewBalance , ending_balance)

    def test_5_to_deposit_invalid_input_negative_amount(self):
        test_client = app.test_client()
        with test_client as c:
            respons = c.post(
                '/transactions/deposit', 
                data = {'account_id':'1', 'amount':'-1','operation':"1"})
            self.assertNotEqual(respons.status_code , 302)
    
    def test_6_to_credit_invalid_input_amount_more_then_balance_on_account(self):
        test_client = app.test_client()
        with test_client as c:
            starting_balance = Account.query.where(Account.Id == 1).first().Balance
            more_then_starting_balance = starting_balance + 1

            respons = c.post(
                '/transactions/credit', 
                data = {'account_id':'1', 'amount':f'{more_then_starting_balance}','operation':"1"})
            self.assertNotEqual(respons.status_code , 302)

            # Assumpion that no transactions is ever deleted
            latest_transaction_for_account_1 = Transaction.query.where(
                                            Transaction.AccountId == 1).order_by(
                                            Transaction.Id.desc()).first()
            self.assertEqual(latest_transaction_for_account_1.NewBalance , starting_balance)

    def test_7_to_credit_invalid_input_negative_amount(self):
        test_client = app.test_client()
        with test_client as c:
            account_1 = Account.query.where(Account.Id == 1).first()
            starting_balance = account_1.Balance

            respons = c.post(
                '/transactions/credit', 
                data = {'account_id':'1', 'amount':'-1','operation':"1"})
            self.assertNotEqual(respons.status_code , 302)

            # Assumpion that no transactions is ever deleted
            latest_transaction_for_account_1 = Transaction.query.where(
                                            Transaction.AccountId == 1).order_by(
                                            Transaction.Id.desc()).first()
            self.assertEqual(latest_transaction_for_account_1.NewBalance , starting_balance)

    def test_8_to_transfer_within_bank_valid_input(self):
        test_client = app.test_client()
        with test_client as c:
            random_amount = randint(1,10)

            starting_balance_account_1 = Account.query.where(Account.Id == 1).first().Balance
            ending_balance_account_1 = starting_balance_account_1 - random_amount
            
            starting_balance_account_2 = Account.query.where(Account.Id == 2).first().Balance
            ending_balance_account_2 = starting_balance_account_2 + random_amount

            respons = c.post(
                '/transactions/transfer', 
                data = {'account_id':'1', 'amount':f'{random_amount}','account_id_debit':"2"})
            self.assertEqual(respons.status_code , 302)

            self.assertEqual(
                ending_balance_account_1,
                Account.query.where(Account.Id == 1).first().Balance
                )
            self.assertEqual(
                ending_balance_account_2,
                Account.query.where(Account.Id == 2).first().Balance
                )

            # Assumpion that no transactions is ever deleted
            latest_transaction_for_account_1 = Transaction.query.where(
                                            Transaction.AccountId == 1).order_by(
                                            Transaction.Id.desc()).first()
            self.assertEqual(latest_transaction_for_account_1.Amount , random_amount)
            self.assertEqual(latest_transaction_for_account_1.NewBalance , ending_balance_account_1)
            
            latest_transaction_for_account_2 = Transaction.query.where(
                                            Transaction.AccountId == 2).order_by(
                                            Transaction.Id.desc()).first()
            self.assertEqual(latest_transaction_for_account_2.Amount , random_amount)
            self.assertEqual(latest_transaction_for_account_2.NewBalance , ending_balance_account_2)

    def test_9_to_transfer_within_bank_invalid_input_try_transfer_more_then_on_account_balance(self):
        test_client = app.test_client()
        with test_client as c:

            starting_balance_account_1 = Account.query.where(Account.Id == 1).first().Balance
            starting_balance_account_2 = Account.query.where(Account.Id == 2).first().Balance

            amount_try_to_transfer_from_account_1 = starting_balance_account_1 +1

            respons = c.post(
                '/transactions/transfer', 
                data = {'account_id':'1', 'amount':f'{amount_try_to_transfer_from_account_1}','account_id_debit':"2"})
            self.assertNotEqual(respons.status_code , 302)

            self.assertEqual(
                starting_balance_account_1,
                Account.query.where(Account.Id == 1).first().Balance
                )
            self.assertEqual(
                starting_balance_account_2,
                Account.query.where(Account.Id == 2).first().Balance
                )

            # Assumpion that no transactions is ever deleted
            latest_transaction_for_account_1 = Transaction.query.where(
                                            Transaction.AccountId == 1).order_by(
                                            Transaction.Id.desc()).first()
            self.assertEqual(latest_transaction_for_account_1.NewBalance , starting_balance_account_1)
            
            latest_transaction_for_account_2 = Transaction.query.where(
                                            Transaction.AccountId == 2).order_by(
                                            Transaction.Id.desc()).first()
            self.assertEqual(latest_transaction_for_account_2.NewBalance , starting_balance_account_2)

    def test_10_to_transfer_within_bank_invalid_input_negative_amount(self):
        test_client = app.test_client()
        with test_client as c:

            starting_balance_account_1 = Account.query.where(Account.Id == 1).first().Balance
            starting_balance_account_2 = Account.query.where(Account.Id == 2).first().Balance

            respons = c.post(
                '/transactions/transfer', 
                data = {'account_id':'1', 'amount':'-1','account_id_debit':"2"})
            self.assertNotEqual(respons.status_code , 302)

            self.assertEqual(
                starting_balance_account_1,
                Account.query.where(Account.Id == 1).first().Balance
                )
            self.assertEqual(
                starting_balance_account_2,
                Account.query.where(Account.Id == 2).first().Balance
                )

            # Assumpion that no transactions is ever deleted
            latest_transaction_for_account_1 = Transaction.query.where(
                                            Transaction.AccountId == 1).order_by(
                                            Transaction.Id.desc()).first()
            self.assertEqual(latest_transaction_for_account_1.NewBalance , starting_balance_account_1)
            
            latest_transaction_for_account_2 = Transaction.query.where(
                                            Transaction.AccountId == 2).order_by(
                                            Transaction.Id.desc()).first()
            self.assertEqual(latest_transaction_for_account_2.NewBalance , starting_balance_account_2)



if __name__ == "__main__":
    unittest.main()