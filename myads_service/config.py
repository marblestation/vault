MYADS_APP_SECRET_KEY = 'fake'
MYADS_OAUTH_CLIENT_TOKEN = 'to be provided'
MYADS_VERSION = 'v0.1' # Arbitrary string identifying the service (will be returned in the headers)

SQLALCHEMY_DATABASE_URI = 'sqlite:///'
#SQLALCHEMY_BINDS = {
#    'myads':        ':memory:'
#}
SQLALCHEMY_ECHO = False

# location of the remote solr-microservice
MYADS_SOLR_QUERY_ENDPOINT = 'https://api.adsabs.harvard.edu/v1/search/query'
MYADS_SOLR_BIGQUERY_ENDPOINT = 'https://api.adsabs.harvard.edu/v1/search/bigquery'

use_flask_db_url = True