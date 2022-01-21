from turtle import home
from flask import Flask, render_template
from views.home import home
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from models import db, seedData, Account, Customer, Transaction
from flask_migrate import Migrate, upgrade


app = Flask(__name__)
app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(home, url_prefix='/')

@app.route("/table")
def table():
    return render_template('tabledataBasetemplate.html', customer_list = Customer.query.limit(100))




if __name__ == "__main__":
    with app.app_context():
        upgrade()
    seedData(db)
    app.run()