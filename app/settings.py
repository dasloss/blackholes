"""
Global settings for your application.
"""

# Environment                                                                  
environment = 'cloud'
type_of_stripe = 'testing'

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

# Stripe settings
if type_of_stripe == 'testing':
    PUBLISHABLE_KEY = 'pk_test_BHJHfU6oDQPwau8nycmdeSHS'
    SECRETIVE_KEY = 'sk_test_K0tiWSjJkcQ4lwMSm9JZqxPk'
    CLIENT_ID = 'ca_0zTQLhLISbr3wUAOCqRNZKqjF1L0Bcw9'
elif type_of_stripe == 'live':
    PUBLISHABLE_KEY = 'pk_live_zybWa72LBd4hdkLYujAuJH1d'
    SECRETIVE_KEY = 'sk_live_wXFnTotu80T6IfMwtf4rwB69'
    CLIENT_ID = 'ca_0zTQJmys4auWsqsMABMzUorTXzWkd3Dx'

# App settings                                                                 
SECRET_KEY = '143h1234g12l3g123l5kgh123jg123kjhg1231g512j13477ljhgvcz452'
