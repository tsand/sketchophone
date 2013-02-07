import os

FACEBOOK_APP_ID = '211731262298555'
FACEBOOK_APP_SECRET = 'ce08a9ba2a5fc6852a5fe3f9c1ac8e8d'

# Change facebook app when running locally
if os.environ['SERVER_SOFTWARE'].startswith('Development'):
    FACEBOOK_APP_ID = '152685264887279'
    FACEBOOK_APP_SECRET = '0a90a2d2277e302fbc8b7e54f540cb19'

PASSWORD_LENGTH = 6



