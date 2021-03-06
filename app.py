from flask import Flask
from views import home,customers,accounts, transactions, admin
from models import db, seedData
from flask_migrate import Migrate, upgrade
from models import User, user_manager



app = Flask(__name__)
app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app, db)  
user_manager.app = app
user_manager.init_app(app,db,User)

app.register_blueprint(home, url_prefix='/')
app.register_blueprint(customers, url_prefix='/customer')
app.register_blueprint(accounts, url_prefix='/account')
app.register_blueprint(transactions,url_prefix='/transactions')
app.register_blueprint(admin,url_prefix='/admin')





if __name__ == "__main__":
    with app.app_context():
        upgrade()
        seedData(db)
    app.run()