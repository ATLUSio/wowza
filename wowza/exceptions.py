"""
Exception definitions
"""

class InvalidParamDict(Exception):
    """
    Class for exceptions due to the `param_dict` not being in the 
    right format.
    Desired parameters for update should be passed in as a dictionary like
    the following:
    {'transcoder_type': 'transcoded'}
    """
    def __init__(self, error):
        Exception.__init__(self, error['message'])
        self.code = 400


class InvalidParameter(Exception):
    """
    Class for exceptions due to invalid parameters.
    """
    def __init__(self, error):
        Exception.__init__(self, error['message'])
        self.code = 400

class MissingParameter(Exception):
	"""
	Class for exceptions due to missing required parameters.
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 400

class NoApiKey(Exception):
	"""
	Class for exceptions due to missing API Key
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 401

class NoAccessKey(Exception):
	"""
	Class for exceptions due to missing Access Key
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 401

class InvalidApiKey(Exception):
	"""
	Class for exceptions due to invalid API Key
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 401

class InvalidAccessKey(Exception):
	"""
	Class for exceptions due to invalid Access Key
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 401

class BadAccountStatus(Exception):
	"""
	Class for exceptions due to account being in bad status
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 401

class FeatureNotEnabled(Exception):
	"""
	Class for exceptions due to disabled features
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 401

class TrialExceeded(Exception):
	"""
	Class for exceptions due to maxed out trial account
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 401

class RecordUnaccessible(Exception):
	"""
	Class for exceptions due to unaccessible records due to
	insufficient permissions
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 403

class RecordNotFound(Exception):
	"""
	Class for exceptions due to records not found
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 404

class RecordDeleted(Exception):
	"""
	Class for exceptions due to records being deleted
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 410

class RecordInvalid(Exception):
	"""
	Class for exceptions due to invalid records
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 422

class InvalidInteraction(Exception):
	"""
	Class for exceptions due to invalid interactions
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 422

class InvalidStateChange(Exception):
	"""
	Class for exceptions due to invalid state changes.
	i.e. attempting to stop a stream that's not running
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 422

class ConnectionCodeNotSupported(Exception):
	"""
	Class for exceptions due to connection code regeneration attempts with
	providers who do not use connection codes (i.e. akamai)
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 405

class TokenAuthBusy(Exception):
	"""
	Class for exceptions due to outstanding token auth requests being processed
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 423

class GeoblockingBusy(Exception):
	"""
	Class for exceptions due to outstanding geoblocking requests being processed
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 423

class LimitReached(Exception):
	"""
	Class for exceptions caused by reaching the limits of the account
	"""
	def __init__(self, error):
		Exception.__init__(self, error['message'])
		self.code = 409
