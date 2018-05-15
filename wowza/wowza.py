import json, time
from . import session
from . import WOWZA_API_KEY, WOWZA_ACCESS_KEY, WOWZA_BASE_URL
from wowza.exceptions import InvalidParamDict, InvalidParameter, MissingParameter, \
    InvalidInteraction, InvalidStateChange, TokenAuthBusy, GeoblockingBusy, \
    LimitReached


class LiveStreams(object):
    """
    Class to interface with the following Wowza endpoints:
    /api/v1/live_streams/
    /api/v1/stream_sources/
    /api/v1/stream_targets/
    """

    def __init__(self,
        base_url=WOWZA_BASE_URL,
        api_key=WOWZA_API_KEY,
        access_key=WOWZA_ACCESS_KEY):
        self.id = id
        self.base_url = base_url
        self.headers = {
            'wsc-api-key': WOWZA_API_KEY,
            'wsc-access-key': WOWZA_ACCESS_KEY,
            'content-type': 'application/json'
        }

    def info(self, stream_id=None, options=None):
        """
        Used to gather info on all streams associated with an account or
        with a particular live stream.
        When called without inputting a stream_id, it'll return all streams
        associated with the account.
        Options: state, stats, thumbnail_url
        """
        if options and not stream_id:
            raise InvalidParameter({
                'message': 'When getting optional info on a stream, a \
                stream_id needs to be provided.'
            })
        path = self.base_url + 'live_streams/'
        if stream_id:
            path = path + stream_id
        if options:
            path = path + "/{}".format(options)
        response = session.get(path, headers=self.headers)
        return response.json()

    def create(self, param_dict):
        """
        Used to create a new live stream.
        Valid parameters:
            name, transcoder_type, billing_mode, broadcast_location,
            encoder, delivery_method, aspect_ratio_width, aspect_ratio_height
        """
        required_params = [
            'name', 'broadcast_location', 'encoder',
            'aspect_ratio_height', 'aspect_ratio_width'
        ]
        for key in required_params:
            if key not in param_dict:
                raise MissingParameter({
                    'message': 'Missing parameter [{}]. Cannot create \
                     live stream.'.format(key)
                })
        param_dict = {
            'live_stream': param_dict
        }
        path = self.base_url + 'live_streams/'
        response = session.post(
            path,
            json.dumps(param_dict),
            headers=self.headers
        )
        return response.json()

    def update(self, stream_id, param_dict):
        """
        Used to update a live stream.
        Expects a dictionary with key-value pairs of the parameter to change
        and the value to change it to.
        """
        if isinstance(param_dict, dict):
            param_dict = {
                'live_stream': param_dict
            }
            path = self.base_url + 'live_streams/{}'.format(stream_id)
            response = session.patch(path, json.dumps(param_dict), headers=self.headers)
            return response.json()
        else:
            raise InvalidParamDict({
                'message': 'Desired parameters for update should be passed in \
                as a dictionary with key-value pairs. \
                i.e. {\'transcoder_type\': \'transcoded\'}'
            })

    def delete(self, stream_id):
        """
        Used to delete a live stream.
        """
        state = self.info(stream_id, 'state')['live_stream']['state']
        if state is not 'started':
            path = self.base_url + 'live_streams/{}'.format(stream_id)
            response = session.delete(path, headers=self.headers)
            return response
        else:
            raise InvalidInteraction({
                'message': 'Cannot delete a running event. Stop the event first \
                and try again.'
            })

    def start(self, stream_id):
        """
        Used to start a live stream
        """
        path = self.base_url + "live_streams/{}/start".format(stream_id)
        response = session.put(path, data='', headers=self.headers)
        return response.json()

    def reset(self, stream_id):
        """
        Used to reset a live stream
        """
        path = self.base_url + "live_streams/{}/reset".format(stream_id)
        response = session.put(path, data='', headers=self.headers)
        if 'meta' in response.json():
            if response.json()['meta']['code'] == 'ERR-422-InvalidInteraction':
                raise InvalidInteraction({
                    'message': 'Unable to reset stream. Invalid state for resetting.'
                }) 
        return response.json()

    def stop(self, stream_id):
        """
        Used to stop a live stream
        """
        state = self.info(stream_id, 'state')['live_stream']['state']
        if state == 'started':
            path = self.base_url + "live_streams/{}/stop".format(stream_id)
            response = session.put(path, data='', headers=self.headers)
            if 'meta' in response.json():
                if response.json()['meta']['code'] == 'ERR-422-InvalidInteraction':
                    raise InvalidInteraction({
                        'message': 'Unable to stop stream. Invalid state for stopping.'
                    }) 
        else:
            raise InvalidStateChange({
                'message': 'Cannot stop a live stream that is not running.'
            })
        return response.json()

    def stats(self, stream_id):
        """
        This operation returns a hash of metrics keys, each of which identifies a status, text description, unit, and value
        """
        path = self.base_url + "live_streams/{}/stats".format(stream_id)
        response = session.get(path, headers=self.headers)
        return response.json()


    def new_code(self, stream_id):
        """
        Used to generate a new connection code for a live stream
        """
        path = self.base_url + "live_streams/{}/regenerate_connection_code".format(stream_id)
        response = session.put(path, data='', headers=self.headers)
        return response.json()

    def regenerate_connection_code(self, stream_id):
        """
        Same as #new_code()
        """
        return self.new_code(stream_id)


class StreamSources(object):
    """
    Class to interface with the following Wowza endpoints:
    /api/v1/stream_sources/
    """

    def __init__(self,
        base_url=WOWZA_BASE_URL + 'stream_sources/',
        api_key=WOWZA_API_KEY,
        access_key=WOWZA_ACCESS_KEY):
        self.id = id
        self.base_url = base_url
        self.headers = {
            'wsc-api-key': WOWZA_API_KEY,
            'wsc-access-key': WOWZA_ACCESS_KEY,
            'content-type': 'application/json'
        }

    def info(self, source_id=None):
        """
        Used to get information regarding all stream sources or to get
        information on a particular source
        """
        path = self.base_url
        path = "{}/{}".format(path, source_id) if source_id else path
        response = session.get(path, headers=self.headers)
        return response.json()

    def source(self, source_id):
        """
        Used to get information on one particular source
        """
        return self.info(source_id)

    def create(self, param_dict):
        """
        Used to create a source
        """
        if isinstance(param_dict, dict):
            path = self.base_url
            param_dict = {
                'stream_source': param_dict
            }
            response = session.post(path, json.dumps(param_dict),
                headers=self.headers)
            return response.json()
        else:
            return InvalidParamDict({
                    'message': 'The provided parameter dictionary is not valid.'
            })

    def update(self, source_id, param_dict):
        """
        Used to update the details associated with a particular source
        """
        if isinstance(param_dict, dict):
            path = self.base_url + source_id
            param_dict = {
                'stream_source': param_dict
            }
            response = session.patch(path, json.dumps(param_dict),
                headers=self.headers)
            return response.json()
        else:
            return InvalidParamDict({
                    'message': 'The provided parameter dictionary is not valid.'
            })

    def delete(self, source_id):
        """
        Used to delete a particular source
        """
        path = self.base_url + source_id
        response = session.delete(path, headers=self.headers)
        return response


class StreamTargets(object):
    """
    Class to interface with the following Wowza endpoints:
    /api/v1/stream_targets
    """

    def __init__(self,
        base_url=WOWZA_BASE_URL + 'stream_targets/',
        api_key=WOWZA_API_KEY,
        access_key=WOWZA_ACCESS_KEY):
        self.id = id
        self.base_url = base_url
        self.headers = {
            'wsc-api-key': WOWZA_API_KEY,
            'wsc-access-key': WOWZA_ACCESS_KEY,
            'content-type': 'application/json'
        }

    def info(self, stream_target_id=None):
        """
        Used to get information regarding all stream targets or a particular stream
        based on the stream target ID
        """
        path = self.base_url
        path = "{}{}".format(path, stream_target_id) if stream_target_id else path
        response = session.get(path, headers=self.headers)
        return response.json()

    def create(self, param_dict):
        """
        Used to create a new stream
        """
        if isinstance(param_dict, dict):
            path = self.base_url
            param_dict = {
                'stream_target': param_dict
            }
            response = session.post(path, json.dumps(param_dict), 
                headers=self.headers)
            if 'meta' in response.json():
                if 'LimitReached' in response.json()['meta']['code']:
                    raise LimitReached({
                        'message': response.json()['meta']['message']
                    })
            return response.json()
        else:
            return InvalidParamDict({
                'message': 'Invalid parameter dictionary provided.'
            })

    def update(self, stream_target_id, param_dict):
        """
        Used to update details associated with a particular stream target
        """
        if isinstance(param_dict, dict):
            path = self.base_url + stream_target_id
            param_dict = {
                'stream_target': param_dict
            }
            response = session.patch(path, json.dumps(param_dict),
                headers=self.headers)
            return response.json()
        else:
            raise InvalidParamDict({
                'message': 'Invalid parameter dictionary provided.'
            })

    def delete(self, stream_target_id):
        """
        Used to delete a given stream target by ID
        """
        path = self.base_url + stream_target_id
        response = session.delete(path, headers=self.headers)
        return response

    def new_code(self, stream_target_id):
        """
        Used to create a new connection code for a stream target
        """
        path = self.base_url + '{}/regenerate_connection_code'.format(stream_target_id)
        response = session.put(path, data='', headers=self.headers)
        return response.json()

    def regenerate_connection_code(self, stream_target_id):
        """Same as #new_code()"""
        return self.new_code(stream_target_id)

    def token_auth_info(self, stream_target_id):
        """
        Get the details of the token authorization applied to a stream target
        """
        path = self.base_url + '{}/token_auth'.format(stream_target_id)
        response = session.get(path, headers=self.headers)
        return response.json()

    def token_auth(self, stream_target_id):
        """Same as #token_auth_info()"""
        return self.token_auth_info(stream_target_id)

    def create_token_auth(self, stream_target_id, param_dict):
        """
        Create token authorization for a stream target
        """
        if isinstance(param_dict, dict):
            path = self.base_url + '{}/token_auth'.format(stream_target_id)
            param_dict = {
                'token_auth': param_dict
            }
            response = session.post(path, json.dumps(param_dict),
                headers=self.headers)
            return response.json()
        else:
            raise InvalidParamDict({
                'message': 'Invalid parameter dictionary provided.'
            })

    def update_token_auth(self, stream_target_id, param_dict, wait=False):
        """
        Used to update details associated with a token authorization
        """
        if isinstance(param_dict, dict):
            path = self.base_url + '{}/token_auth'.format(stream_target_id)
            param_dict = {
                'token_auth': param_dict
            }
            response = session.patch(path, json.dumps(param_dict),
                headers=self.headers)
            if ('meta' in response.json()) and wait: # if we want to try again
                if response.json()['meta']['code'] == 'ERR-423-TokenAuthBusy':
                    while 'meta' in response.json():
                        response = session.patch(path, json.dumps(param_dict),
                            headers=self.headers)
                        time.sleep(5)
                    return response.json()
            else:
                raise TokenAuthBusy({
                    'message': 'The stream target is already processing a \
                    token auth request. Please try again later, or try \
                    submitting your request with the wait=True parameter.'
                    })
            return response.json()
        else:
            raise InvalidParamDict({
                'message': 'Invalid parameter dictionary provided.'
            })

    def properties(self, stream_target_id, property_id=None):
        """
        Used to get the properties associated with a particular stream target.
        Can be used to get a particular property
        """
        path = self.base_url + '{}/properties'.format(stream_target_id)
        path = "{}/{}".format(path, property_id) if property_id else path
        response = session.get(path, headers=self.headers)
        return response.json()

    def create_property(self, stream_target_id, param_dict):
        """
        Used to create a property for a stream target
        """
        if isinstance(param_dict, dict):
            path = self.base_url + '{}/properties'.format(stream_target_id)
            param_dict = {
                'property': param_dict
            }
            response = session.post(path, json.dumps(param_dict),
                headers=self.headers)
            return response.json()
        else:
            raise InvalidParamDict({
                'message': 'Invalid parameter dictionary provided.'
            })

    def delete_property(self, stream_target_id, property_id):
        """
        Used to delete a property from a stream target
        """
        path = self.base_url + '{}/properties/{}'\
            .format(stream_target_id, property_id)
        response = session.delete(path, headers=self.headers)
        return response

    def geoblock(self, stream_target_id):
        """
        Get geoblocking details applied to a stream target
        NOTE: WOWZA ALPHA FEATURE
        """
        path = self.base_url + '{}/geoblock'.format(stream_target_id)
        response = session.get(path, headers=self.headers)
        return response.json()

    def create_geoblock(self, stream_target_id, param_dict):
        """
        Create a geoblock location for a stream target
        NOTE: WOWZA ALPHA FEATURE
        """
        if isinstance(param_dict, dict):
            path = self.base_url + '{}/geoblock'.format(stream_target_id)
            param_dict = {
                'geoblock': param_dict
            }
            response = session.post(path, json.dumps(param_dict),
                headers=self.headers)
            return response.json()
        else:
            raise InvalidParamDict({
                'message': 'Invalid parameter dictionary provided.'
            })

    def update_geoblock(self, stream_target_id, param_dict, wait=False):
        """ Updates a geoblocked location """
        if isinstance(param_dict, dict):
            path = self.base_url + '{}/geoblock'.format(stream_target_id)
            param_dict = {
                'geoblock': param_dict
            }
            response = session.patch(path, json.dumps(param_dict),
                headers=self.headers)
            # if we want to wait until we're able to make the update
            # it may take up to 30 minutes for mutability after creation
            if ('meta' in response.json()) and wait:
                if response.json()['meta']['code'] == 'ERR-423-GeoblockingBusy':
                    while 'meta' in response.json():
                        response = session.patch(path, json.dumps(param_dict),
                            headers=self.headers)
                        time.sleep(5)
                    return response.json()
            else:
                raise GeoblockingBusy({
                    'message': 'The stream target is already processing a \
                    geoblocking request. Please try again later, or try \
                    submitting your request with the wait=True parameter.'
                    })
            return response.json()
        else:
            raise InvalidParamDict({
                'message': 'Invalid parameter dictionary provided.'
            })


class Players(object):
    """
    Class to interface with the following Wowza endpoints:
    /api/v1/players/
    """
    def __init__(self,
        base_url=WOWZA_BASE_URL + 'players/',
        api_key=WOWZA_API_KEY,
        access_key=WOWZA_ACCESS_KEY):
        self.id = id
        self.base_url = base_url
        self.headers = {
            'wsc-api-key': WOWZA_API_KEY,
            'wsc-access-key': WOWZA_ACCESS_KEY,
            'content-type': 'application/json'
        }

    def info(self, player_id=None, option=None):
        """
        Used to get information on a given player or all players associated
        with an account
        Valid options: 
        """
        path = self.base_url
        path = "{}{}".format(path, player_id) if player_id else path
        path = "{}/{}".format(path, option) if option else path
        response = session.get(path, headers=self.headers)
        return response.json()

    def update(self, player_id, param_dict):
        """
        Used to update parameters on a given player
        """
        missing_params = [
            'Player ID' if not player_id else None,
            'Parameter Dictionary' if not param_dict else None
        ]
        while None in missing_params:
            missing_params.remove(None)
        if missing_params:
            raise MissingParameter({
                'message': 'Missing {}.'.format(missing_params)
            })
        param_dict = {
            'player': param_dict
        }
        path = "{}{}".format(self.base_url, player_id)
        response = session.patch(path, json.dumps(param_dict), headers=self.headers)
        return response.json()

    def rebuild(self, player_id):
        """
        Used to rebuild a given player
        """
        path = "{}{}/rebuild".format(self.base_url, player_id)
        response = session.post(path, data='', headers=self.headers)
        return response.json()

    def urls(self, player_id, option=None, url_id=None, param_dict=None):
        """
        Used to interact with the /players/:id/urls/ endpoint
        """
        path = self.base_url + player_id + '/urls/'
        if option:
            if option.upper() == "NEW":
                # Option 'new' means create a new player URL
                required_params = [
                    'url', 'bitrate'
                ]
                for param in required_params:
                    if param not in param_dict:
                        raise MissingParameter({
                            'message': 'Missing [{}] parameter from parameter \
                            dictionary.'
                        })
                param_dict = {
                    'url': param_dict
                }
                response = session.post(path, data=json.dumps(param_dict), headers=self.headers)
            elif url_id and not option:
                # No option + URL ID = GET on that URL by ID
                response = session.get(path, headers=self.headers)
            elif option.upper() == 'delete'.upper(): # DELETE is a keyword
                if not url_id:
                    raise MissingParameter({
                        'message': 'URL_ID needs to be provided when deleting a player URL.'
                    })
                path = path + url_id
                response = session.delete(path, headers=self.headers)
                return response
            elif option.upper() == 'update'.upper(): # UPDATE is a keyword
                missing_params = [
                    'URL ID' if not url_id else None,
                    'Parameter Dictionary' if not param_dict else None
                ]
                while None in missing_params:
                    missing_params.remove(None)
                if missing_params:
                    raise MissingParameter({
                        'message': '{} needs to be provided when updating a player URL.'\
                            .format(missing_params)
                    })
                path = path + url_id
                param_dict = {
                    'url': param_dict
                }
                response = session.patch(path, json.dumps(param_dict),headers=self.headers)
        else:
            if url_id:
                path = path + url_id
            response = session.get(path, headers=self.headers)
        return response.json()

    def url_delete(self, player_id, url_id):
        """
        Used to delete a particular URL by id
        """
        return self.urls(player_id, 'delete', url_id)


class Recordings(object):
    """
    Class to interface with the following Wowza endpoints:
    /api/v1/recordings/
    """
    def __init__(self,
        base_url=WOWZA_BASE_URL + 'recordings/',
        api_key=WOWZA_API_KEY,
        access_key=WOWZA_ACCESS_KEY):
        self.id = id
        self.base_url = base_url
        self.headers = {
            'wsc-api-key': WOWZA_API_KEY,
            'wsc-access-key': WOWZA_ACCESS_KEY,
            'content-type': 'application/json'
        }

    def info(self, rec_id=None, option=None):
        """
        Used to get information on all recordings or on one recording
        """
        path = self.base_url + rec_id if rec_id else self.base_url
        if option and option == 'state':
            if rec_id:
                path = path + '/state'
            else:
                raise MissingParameter({
                    'message': 'Recording ID needs to be provided when \
                    getting the state of a recording.'
                })
        response = session.get(path, headers=self.headers)
        return response.json()

    def delete(info, rec_id):
        """
        Used to delete a recording
        """
        path = self.base_url + rec_id
        response = session.delete(path, headers=self.headers)
        return response


class Schedules(object):
    """
    Class to interface with the following Wowza endpoints:
    /api/v1/schedules/
    """
    def __init__(self,
        base_url=WOWZA_BASE_URL + 'schedules/',
        api_key=WOWZA_API_KEY,
        access_key=WOWZA_ACCESS_KEY):
        self.id = id
        self.base_url = base_url
        self.headers = {
            'wsc-api-key': WOWZA_API_KEY,
            'wsc-access-key': WOWZA_ACCESS_KEY,
            'content-type': 'application/json'
        }

    def info(self, sched_id=None, option=None):
        """
        Used to get information on all schedules or a particular schedule.
        Can also be used to get the state of a particular schedule.
        """
        path = self.base_url
        path = path + sched_id if sched_id else path
        if option:
            if not sched_id:
                raise MissingParameter({
                    'message': 'Need schedule ID if getting the state of a schedule.'
                })
            path = path + "/state"
        response = session.get(path, headers=self.headers)
        return response.json()

    def create(self, param_dict):
        """
        Used to create a new schedule
        """
        path = self.base_url
        '''
        # Removing this check for now because the Wowza API for this endpoint doesn't seem
        # to know what it wants.
        for parameter in [
            'transcoder_id', 'name', 'action_type',
            'start_transcoder', 'stop_transcoder']:
            if parameter not in param_dict:
                raise MissingParameter({
                    'message': 'Missing parameter [{}] from the parameter \
                    dictionary.'.format(parameter)
                })
        '''
        param_dict = {
            'schedule': param_dict
        }
        response = session.post(path, json.dumps(param_dict), headers=self.headers)
        return response.json()

    def update(self, sched_id, param_dict):
        """
        Used to update the details associated with a specific schedule
        """
        path = self.base_url + sched_id
        if isinstance(param_dict, dict):
            param_dict = {
                'schedule': param_dict
            }
            response = session.patch(path, json.dumps(param_dict), headers=self.headers)
            return response.json()
        else:
            raise InvalidParamDict({
                'message': 'Param_dict needs to be a valid dictionary.'
            })

    def delete(self, sched_id):
        """
        Used to delete a particular schedule
        """
        path = "{}{}/delete".format(self.base_url, sched_id)
        response = session.delete(path, headers=self.headers)
        return response

    def enable(self, sched_id):
        """
        Used to enable a particular schedule
        """
        path = "{}{}/enable".format(self.base_url, sched_id)
        response = session.put(path, data='', headers=self.headers)
        return response.json()

    def start(self, sched_id):
        """
        Same as #enable()
        """
        return self.enable(sched_id)

    def disable(self, sched_id):
        """
        Used to disable a particular schedule
        """
        path = "{}{}/disable".format(self.base_url, sched_id)
        response = session.put(path, data='', headers=self.headers)
        return response.json()

    def stop(self, sched_id):
        """
        Same as #disable()
        """
        return self.disable(sched_id)

    def toggle(self, sched_id):
        """
        Toggles the state of a schedule
        """
        state = self.info(sched_id, 'state')['schedule']['state']
        print("State: {}".format(state))
        if state == 'enabled':
            return self.disable(sched_id)
        else:
            return self.enable(sched_id)


class Transcoders(object):
    """
    Class to interface with the following Wowza endpoints:
    /api/v1/transcoders/
    """
    def __init__(self,
        base_url=WOWZA_BASE_URL + 'transcoders/',
        api_key=WOWZA_API_KEY,
        access_key=WOWZA_ACCESS_KEY):
        self.id = id
        self.base_url = base_url
        self.headers = {
            'wsc-api-key': WOWZA_API_KEY,
            'wsc-access-key': WOWZA_ACCESS_KEY,
            'content-type': 'application/json'
        }

    def info(self, tran_id=None, option=None, uptime_id=None):
        """
        Get information on all transcoders or a specific transcoder
        Valid options: recordings, schedules, state, stats, thumbnail_url
        """
        path = self.base_url + tran_id if tran_id else self.base_url
        valid_options = [
            'recordings', 'schedules', 'state',
            'stats', 'thumbnail_url'
        ]
        if option:
            if not tran_id:
                raise MissingParameter({
                    'message': 'Transcoder ID is also needed when passing in an \
                    option'
                })
            if option not in valid_options:
                raise InvalidParameter({
                    'message': 'Option provided is invalid. Valid options are: {}'\
                        .format(valid_options)
                })
            path = path + option
        response = session.get(path, headers=self.headers)
        return response.json()

    def uptime(self, tran_id, uptime_id=None, options=None):
        """
        Get details and health metrics for a particular transcoder
        Valid options = current, historic
        """
        path = self.base_url + "{}/uptimes/"
        if options == "current":
            path = path + tran_id + "/metrics/current"
        elif options == "historic":
            path = path + tran_id + "/metrics/historic"
        else:
            path = path + tran_id
        response = session.get(path, headers=self.headers)
        return response.json()

    def create(self, param_dict):
        """
        Used to create a transcoder.
        """
        path = self.base_url
        for parameter in ['name', 'transcoder_type', 'billing_mode',
            'broadcast_location', 'protocol', 'delivery_method']:
            if parameter not in param_dict:
                raise MissingParameter({
                    'message': 'Parameter [{}] missing from the parameter \
                    dictionary.'.format(parameter)
                })
        param_dict = {
            'transcoder': param_dict
        }
        response = session.post(path, json.dumps(param_dict), headers=self.headers)
        return response.json()

    def delete(self, tran_id):
        """
        Used to delete a transcoder.
        Usage => delete('5jfg91m')
        """
        path = self.base_url + tran_id
        response = session.delete(path, headers=self.headers)
        return response


class Usage(object):
    """
    Class to interface with the following Wowza endpoints:
    /api/v1/usage/
    """
    def __init__(self,
        base_url=WOWZA_BASE_URL + 'usage/',
        api_key=WOWZA_API_KEY,
        access_key=WOWZA_ACCESS_KEY):
        self.id = id
        self.base_url = base_url
        self.headers = {
            'wsc-api-key': WOWZA_API_KEY,
            'wsc-access-key': WOWZA_ACCESS_KEY,
            'content-type': 'application/json'
        }

    def network(self, option):
        """
        Used to get statistics on for network usage.
        Valid options: sources, targets, transcoders
        """
        valid_options = ['sources', 'targets', 'transcoders']
        if option not in valid_options:
            raise InvalidParameter({
                'message': 'Invalid option provided. Valid options are: {}'\
                    .format(valid_options)
                })
        path_suffix = "stream_sources" if option == "sources" else \
            ("stream_targets" if option == "targets" else option)
        path = self.base_url + path_suffix
        response = session.get(path, headers=self.headers)
        return response.json()

    def storage(self):
        """
        Used to get the peak recording storage for the account
        """
        path = self.base_url + 'storage/peak_recording'
        response = session.get(path, headers=self.headers)
        return response.json()

    def transcoders(self):
        """
        Used to get the stream processing time for the account
        """
        path = self.base_url + 'time/transcoders'
        response = session.get(path, headers=self.headers)
        return response.json()

    def viewer_data(self, stream_target_id):
        """
        Used to get the viewer data of a stream target
        """
        path = self.base_url + 'viewer_data/stream_targets/{}'\
            .format(stream_target_id)
        response = session.get(path, headers=self.headers)
        return response.json()
