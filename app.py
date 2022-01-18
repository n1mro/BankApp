from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from models import db, seedData, Account, Customer, Transaction
from flask_migrate import Migrate, upgrade


app = Flask(__name__)
app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def index():
    index_body_parameters = {
    "number_of_customers": Customer.query.count(),
    "number_of_accounts": Account.query.count(),
    "total_amount_in_accounts": db.session.query(func.sum(Account.Balance)).scalar()
    }
    print(index_body_parameters)
    return render_template('index.html', **index_body_parameters)


if __name__ == "__main__":
    with app.app_context():
        upgrade()
    seedData(db)
    app.run()