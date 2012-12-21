"""
Global settings for your application.
"""

# Environment                                                                  
environment = 'local'

# Database settings                                                            
if environment == 'cloud':
    DB = 'heroku_app10242421'
    DB_HOST = 'ds045897.mongolab.com'
    DB_PORT = 45897
    DB_USER = 'heroku_app10242421'
    DB_PASS = 'a385sddfo3m8shtabta8ir5pb4'
elif environment == 'local':
    DB = 'multidonate'
    DB_HOST = 'localhost'
    DB_PORT = 27017
    DB_USER = 'gfc'                                                         
    DB_PASS = 'gfcpass'                                                      
MONGO_URI='mongodb://heroku_app10242421:a385sddfo3m8shtabta8ir5pb4@ds045897.mongolab.com:45897/heroku_app10242421'

# App settings                                                                 
SECRET_KEY = '143h1234g12l3g123l5kgh123jg123kjhg1231g512j13477ljhgvcz452'
