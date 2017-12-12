import os, requests
from wowza.exceptions import NoApiKey, NoAccessKey

WOWZA_API_KEY = os.environ.get(
	'WOWZA_API_KEY', None
)

WOWZA_ACCESS_KEY = os.environ.get(
	'WOWZA_ACCESS_KEY', None
)

if not WOWZA_API_KEY:
	raise NoApiKey({
		'message': 'API key needed to interact with API!'
	})
if not WOWZA_ACCESS_KEY:
	raise NoAccessKey({
		'message': 'Access key needed to interact with API!'
	})

# Get the production level
WOWZA_PRODUCTION_LEVEL = os.environ.get(
	'WOWZA_PRODUCTION_LEVEL',
	'SANDBOX')

# Set default production level to sandbox
WOWZA_BASE_URL = 'https://api{}.cloud.wowza.com/api/v1/'.format(
	'-sandbox' if WOWZA_PRODUCTION_LEVEL == 'SANDBOX' else ''
)

session = requests.Session()
session.params = {}
session.params['accept'] = 'application/json'

from wowza.wowza import *
