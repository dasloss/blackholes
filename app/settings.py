"""
Global settings for your application.
"""

# Environment                                                                  
environment = 'local'
type_of_stripe = 'testing'

# Database settings                                                            
if environment == 'cloud':
    DB = ''
    DB_HOST = ''
    DB_PORT = 
    DB_USER = ''
    DB_PASS = ''
elif environment == 'local':
    DB = ''
    DB_HOST = 'localhost'
    DB_PORT = 27017
    DB_USER = ''                                                         
    DB_PASS = ''                                                      
MONGO_URI=''

# Stripe settings
if type_of_stripe == 'testing':
    PUBLISHABLE_KEY = ''
    SECRETIVE_KEY = ''
    CLIENT_ID = ''
elif type_of_stripe == 'live':
    PUBLISHABLE_KEY = ''
    SECRETIVE_KEY = ''
    CLIENT_ID = ''

# App settings                                                                 
SECRET_KEY = ''
