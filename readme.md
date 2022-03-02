A simple webb application using Flask and free html template found online. 

This was done as a project for my assignment in school hence it may contain bad practice or plain out right bad implementations as it is made for learning.


In order to get the test to work one must replace (decorators.py , user_manager__settings.py , user_manager.py)
in the flask_user folder with the corresponding files in the test_requirements folder.

Also i have used a .env file for all configuration that needed to hidden from the world such as the SECRET_KEY,SQLALCHEMY_DATABASE_URI_LOCAL and so forth. Then for the app to function correctly it is necessary to either implement the configurations directly in the config.py file or make your own .env file and add the corresponding enviroment variables.
Example: create new file at top level, name it .env and open that file and create the following variables->
    SQLALCHEMY_DATABASE_URI_AZURE = Your sqlalchemy database connection
    SQLALCHEMY_DATABASE_URI_LOCAL = Your sqlalchemy database connection
    SECRET_KEY = sdr2#¤f2fYdfg9sdf83g93292k10kdflk23fk503
    SECRET_KEY_TEST = g0sd9f02okl02g0j0183er8fasjkbnaiusderajSDFqfsefAt



 