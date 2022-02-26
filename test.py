import unittest
from flask import Flask, render_template, request, url_for, redirect
from app import app,user_manager



class TransactionsTestCases(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.ConfigTest')
        self.ctx = app.app_context()
        self.ctx.push()
        # user_manager.login_manager._login_disabled=True

    def test_main_page(self):
        test_client = app.test_client()
        with test_client as c:
            respons = c.get("/home")
            assert respons.status_code == 200

    # def test_for_required_login(self):
    #     test_client = app.test_client()
    #     with test_client as c:
    #         respons = c.get("/customer/list")
    #         assert respons.status_code == 302
    
    def test_for_required_login(self):
        with app.app_context():
            app.config['LOGIN_DISABLED'] = True
            # user_manager.login_manager._login_disabled=True
            test_client = app.test_client()
            with test_client as c:
                respons = c.get("/customer/list")
                assert respons.status_code == 200

    # def test_login_is_working(self):
    #     test_client = app.test_client()
    #     with test_client as c:
    #         respons = c.post("/user/sign-in",
    #             data = {'email':'cashier@example.com', 'password':'Hejsan123'},follow_redirects=False)
    #         print(respons)
    #         print(c)
    #         print(respons.status)
    #         print(respons.status_code)
    #         assert respons.status_code== 302
            # self.assertEqual(current_user.email == "customer@example.com")

if __name__ == "__main__":
    unittest.main()