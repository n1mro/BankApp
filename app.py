from flask import Flask
from views.home import home
from views.listCustomers import listCostumers
from models import db, seedData
from flask_migrate import Migrate, upgrade


app = Flask(__name__)
app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(home, url_prefix='/')
app.register_blueprint(listCostumers, url_prefix='/customers')




if __name__ == "__main__":
    with app.app_context():
        upgrade()
    seedData(db)
    app.run()