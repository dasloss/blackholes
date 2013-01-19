"""
Global settings for your application.
"""

# Environment                                                                  
environment = 'local'

# Database settings                                                            
if environment == 'cloud':
    DB = ''
    DB_HOST = ''
    DB_PORT = 0
    DB_USER = ''
    DB_PASS = ''
elif environment == 'local':
    DB = 'starter'
    DB_HOST = 'localhost'
    DB_PORT = 27017
    DB_USER = ''                                                         
    DB_PASS = ''                                                      
elif environment == 'testing':
    DB = 'testblackholes'
    DB_HOST = 'localhost'
    DB_PORT = 27017
    DB_USER = ''
    DB_PASS = ''
MONGO_URI=''

# App settings                                                                 
SECRET_KEY = ''
