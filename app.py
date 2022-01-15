from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, seedData, Account, Customer, Transaction
from flask_migrate import Migrate, upgrade


app = Flask(__name__)
app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    with app.app_context():
        upgrade()
    seedData(db)
    app.run()