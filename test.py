import unittest
from flask import Flask, render_template, request, url_for, redirect
from app import app
from models import Account,Transaction
from random import randint



class TransactionsTestCases(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.ConfigTest')
        app.config['LOGIN_DISABLED']=True
        self.ctx = app.app_context()
        self.ctx.push()

    def test_main_page(self):
        test_client = app.test_client()
        with test_client as c:
            respons = c.get("/home")
            self.assertEqual(respons.status_code , 200)

    def test_required_login_when_LOGIN_DISABLE_set_to_False(self):
        test_client = app.test_client()
        with test_client as c:
            app.config['LOGIN_DISABLED']=False
            respons = c.get("/customer/list")
            #app.config['LOGIN_DISABLED']=True
            self.assertEqual(respons.status_code , 302)
    
    def test_required_login_when_LOGIN_DISABLE_global_set_to_True(self):
        test_client = app.test_client()
        with test_client as c:
            respons = c.get("/customer/list")
            self.assertEqual(respons.status_code, 200)

    def test_to_deposit_cash_valid_input(self):
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

            self.assertEqual(
                ending_balance,
                Account.query.where(Account.Id == 1).first().Balance
                )

            latest_transaction_for_account_1 = Transaction.query.where(
                                            Transaction.AccountId == 1).order_by(
                                            Transaction.Id.desc()).first()
            self.assertEqual(latest_transaction_for_account_1.Amount , random_amount)
            self.assertEqual(latest_transaction_for_account_1.NewBalance , ending_balance)


if __name__ == "__main__":
    unittest.main()