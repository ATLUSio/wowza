import pytest, os, time, vcr
from wowza import LiveStreams, Players, Recordings, Schedules, \
    Transcoders, StreamSources, StreamTargets
from wowza.exceptions import InvalidParamDict, MissingParameter, \
    TokenAuthBusy, GeoblockingBusy

WOWZA_API_KEY = os.environ.get(
    'WOWZA_API_KEY', None
)

WOWZA_ACCESS_KEY = os.environ.get(
    'WOWZA_ACCESS_KEY', None
)

vcr = vcr.VCR(filter_headers=['wsc-api-key', 'wsc-access-key'])

################
# LIVE STREAMS #
################
wowza_instance = LiveStreams(
    api_key=WOWZA_API_KEY,
    access_key=WOWZA_ACCESS_KEY
)

@vcr.use_cassette('tests/vcr_cassettes/test_stream_create_missing_parameters.yml')
def test_stream_create_missing_parameters():
    """
    Tests an API call to create a live stream without the required
    paremeters. Expects an error.
    """
    with pytest.raises(MissingParameter):
        response = wowza_instance.create({
            'live_stream': {
                'name': 'Test Live Stream'
            }
        })
        assert isinstance(response, dict)
        assert 'meta' in response

@vcr.use_cassette('tests/vcr_cassettes/test_stream_create.yml')
def test_stream_create():
    """
    Tests an API call to create a live stream
    """
    response = wowza_instance.create({
        'name': 'Test1',
        'broadcast_location': 'us_east_s_carolina',
        'encoder': 'wowza_gocoder',
        'aspect_ratio_width': 1280,
        'aspect_ratio_height': 720
    })
    global stream_id
    stream_id = response['live_stream']['id']
    assert isinstance(response, dict)

@vcr.use_cassette('tests/vcr_cassettes/test_stream_update.yml')
def test_stream_update():
    """
    Tests an API call to update the parameters of a live stream
    """
    response = wowza_instance.update(
        stream_id,
        { 'name': 'Test'}
    )
    assert isinstance(response, dict)
    assert response['live_stream']['id'] == stream_id, "The ID should be in the response."

@vcr.use_cassette('tests/vcr_cassettes/test_stream_info.yml')
def test_stream_info():
    """
    Tests an API call to get a live stream's info
    """
    response = wowza_instance.info(stream_id)
    assert isinstance(response, dict)
    assert response['live_stream']['id'] == stream_id, "The ID should be in the response"

@vcr.use_cassette('tests/vcr_cassettes/test_stream_info_state.yml')
def test_stream_info_state():
    """
    Tests an API call to get a live stream's state
    """
    response = wowza_instance.info(stream_id, 'state')
    assert isinstance(response, dict)
    assert 'state' in response['live_stream']

@vcr.use_cassette('tests/vcr_cassettes/test_stream_info_stats.yml')
def test_stream_info_stats():
    """
    Tests an API call to get a live stream's stats
    """
    response = wowza_instance.info(stream_id, 'stats')
    assert isinstance(response, dict)

@vcr.use_cassette('tests/vcr_cassettes/test_stream_info_thumbnail_url.yml')
def test_stream_info_thumbnail_url():
    """
    Tests an API call to get a live stream's stats
    """
    response = wowza_instance.info(stream_id, 'thumbnail_url')
    assert isinstance(response, dict)
    assert 'thumbnail_url' in response['live_stream']

@vcr.use_cassette('tests/vcr_cassettes/test_stream_update_invalid_params.yml')
def test_stream_update_invalid_params():
    """
    Tests a PATCH call to update a live stream without a valid dictionary
    passed in for update_dict
    """
    with pytest.raises(InvalidParamDict):
        response = wowza_instance.update('', '')
        assert isinstance(response, dict)
        assert 'meta' in response

@vcr.use_cassette('tests/vcr_cassettes/test_stream_update_info.yml')
def test_stream_update_info():
    """
    Tests a PATCH call to update a live stream with valid information
    """
    response = wowza_instance.update(
        stream_id,
        {
            "live_stream": {
                "name": "Test"
            }
        }
    )
    assert isinstance(response, dict)
    assert response['live_stream']['name'] == 'Test', "The name in the response should now be 'Test'"

@vcr.use_cassette('tests/vcr_cassettes/test_stream_start.yml')
def test_stream_start():
    """
    Tests a PUT call to start a live stream
    """
    response = wowza_instance.start(stream_id)
    assert isinstance(response, dict)
    assert response['live_stream']['state'] == 'starting', \
        "The starting state should be returned when starting a stream."

@vcr.use_cassette('tests/vcr_cassettes/test_stream_reset.yml')
def test_stream_reset():
    """
    Tests a PUT call to reset a running live stream
    """
    while 1:
        response = wowza_instance.info(stream_id, 'state')
        if response['live_stream']['state'] == "started":
            response = wowza_instance.reset(stream_id)
            assert isinstance(response, dict)
            assert response['live_stream']['state'] == 'resetting', \
                "The returned state on reset should be 'resetting'"
            break

@vcr.use_cassette('tests/vcr_cassettes/test_stream_stop.yml')
def test_stream_stop():
    """
    Tests a PUT call to stop a running live stream
    """
    while 1:
        time.sleep(2)
        response = wowza_instance.info(stream_id, 'state')
        if response['live_stream']['state'] == "started":
            response = wowza_instance.stop(stream_id)
            assert isinstance(response, dict)
            assert response['live_stream']['state'] == "stopped"
            break

@vcr.use_cassette('tests/vcr_cassettes/test_stream_regenerate_connection_code.yml')
def test_stream_regenerate_connection_code():
    """
    Tests a PUT call to regenerate the connection code for a stream
    """
    response = wowza_instance.new_code(stream_id)
    assert isinstance(response, dict)
    assert 'connection_code' in response['live_stream']
    response = wowza_instance.regenerate_connection_code(stream_id)
    assert isinstance(response, dict)
    assert 'connection_code' in response['live_stream']


##################
# STREAM SOURCES #
##################

stream_sources_instance = StreamSources(
    api_key=WOWZA_API_KEY,
    access_key=WOWZA_ACCESS_KEY
)

@vcr.use_cassette('tests/vcr_cassettes/test_stream_sources_create.yml')
def test_stream_sources_create():
    """
    Tests an API call to create a stream source
    """
    response = stream_sources_instance.create({
        'name': 'Test stream source',
        'location': 'us_east_s_carolina'
    })
    assert isinstance(response, dict)
    assert 'stream_source' in response
    global stream_source_id
    stream_source_id = response['stream_source']['id']

@vcr.use_cassette('tests/vcr_cassettes/test_stream_sources_info.yml')
def test_stream_sources_info():
    """
    Tests an API call to get all the stream sources
    """
    response = stream_sources_instance.info()
    assert isinstance(response, dict)
    assert 'stream_sources' in response

@vcr.use_cassette('tests/vcr_cassettes/test_stream_sources_info_specific.yml')
def test_stream_sources_info_specific():
    """
    Tests an API call to get a particular stream source
    """
    response = stream_sources_instance.info(stream_source_id)
    assert isinstance(response, dict)
    assert 'stream_source' in response
    assert stream_source_id == response['stream_source']['id']

@vcr.use_cassette('tests/vcr_cassettes/test_stream_sources_source.yml')
def test_stream_sources_source():
    """
    Tests an API call to get all the stream sources
    """
    response = stream_sources_instance.source(stream_source_id)
    assert isinstance(response, dict)
    assert 'stream_source' in response
    assert stream_source_id == response['stream_source']['id']

@vcr.use_cassette('tests/vcr_cassettes/test_stream_sources_update.yml')
def test_stream_sources_update():
    """
    Tests an API call to update the details associated with a stream source
    """
    response = stream_sources_instance.info(stream_source_id)
    current_name, current_location = \
        response['stream_source']['name'], response['stream_source']['location']
    response = stream_sources_instance.update(
        stream_source_id,
        { 'name': 'New test stream name' }
    )
    name_same = True if response['stream_source']['name'] == \
        current_name else False
    assert isinstance(response, dict)
    assert name_same == False

@vcr.use_cassette('tests/vcr_cassettes/test_stream_sources_delete.yml')
def test_stream_sources_delete():
    """
    Tests an API call to delete a particular stream source
    """
    response = stream_sources_instance.delete(stream_source_id)
    assert response.status_code == 204


##################
# STREAM TARGETS #
##################

stream_targets_instance = StreamTargets(
    api_key = WOWZA_API_KEY,
    access_key = WOWZA_ACCESS_KEY
)

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_create_custom.yml')
def test_stream_targets_create_custom():
    """
    Tests an API call to create a stream target
    """
    response = stream_targets_instance.create({
        'name': 'Test stream target',
        'type': 'CustomStreamTarget',
        'provider': 'akamai_mock',
        'primary_url': 'http://p-ep266276.i.akamaientrypoint.net/12345',
        'stream_name': 'abcd1234',
        'username': '4321dcba',
        'password': 'Theoretically_is_a_secret!'
    })
    assert isinstance(response, dict)
    assert 'stream_target' in response
    response = stream_targets_instance.delete(response['stream_target']['id'])
    assert response.status_code == 204

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_create_wowza.yml')
def test_stream_targets_create_wowza():
    """
    Tests an API call to create a wowza stream target
    """
    response = stream_targets_instance.create({
        'name': 'Test Stream Target Wowza',
        'type': 'WowzaStreamTarget',
        'location': 'us_west_california'
    })
    assert isinstance(response, dict)
    assert 'stream_target' in response
    global stream_target_id
    stream_target_id = response['stream_target']['id']

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_info.yml')
def test_stream_targets_info():
    """
    Tests an API call to get stream targets
    """
    response = stream_targets_instance.info()
    assert isinstance(response, dict)
    assert 'stream_targets' in response

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_info_specific.yml')
def test_stream_targets_info_specific():
    """
    Tests an API call to get a particular stream target
    """
    response = stream_targets_instance.info(stream_target_id)
    assert isinstance(response, dict)
    assert 'stream_target' in response
    assert response['stream_target']['id'] == stream_target_id

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_update.yml')
def test_stream_targets_update():
    """
    Tests an API call to update a particular stream target
    """
    current_name = stream_targets_instance.info(stream_target_id)\
        ['stream_target']['name']
    response = stream_targets_instance.update(
        stream_target_id,
        {
            'name': 'New test stream target name'
        })
    new_name = response['stream_target']['name']
    same_name = True if current_name == new_name else False
    assert isinstance(response, dict)
    assert 'stream_target' in response
    assert same_name == False
    assert response['stream_target']['id'] == stream_target_id

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_regenerate_code.yml')
def test_stream_targets_regenerate_code():
    """
    Tests an API call to regenerate the connection code for a particular
    stream target
    """
    current_code = stream_targets_instance.info(stream_target_id)\
        ['stream_target']['connection_code']
    response = stream_targets_instance\
        .regenerate_connection_code(stream_target_id)
    new_code = response['stream_target']['connection_code']
    same_code = True if current_code == new_code else False
    assert isinstance(response, dict)
    assert 'stream_target' in response
    assert same_code == False

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_new_code.yml')
def test_stream_targets_new_code():
    """
    Tests an API call to get a new connection code for a particular
    stream target
    """
    current_code = stream_targets_instance.info(stream_target_id)\
        ['stream_target']['connection_code']
    response = stream_targets_instance.new_code(stream_target_id)
    new_code = response['stream_target']['connection_code']
    same_code = True if current_code == new_code else False
    assert isinstance(response, dict)
    assert 'stream_target' in response
    assert same_code == False
    
@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_token_auth_create.yml')
def test_stream_targets_token_auth_create():
    """
    Tests an API call to create a new token auth for a particular
    stream target
    """
    response = stream_targets_instance.create_token_auth(
        stream_target_id,
        {
            "enabled": "true",
            "trusted_shared_secret": "499602D2"
        }
    )
    assert isinstance(response, dict)
    assert 'token_auth' in response
    assert response['token_auth']['stream_target_id'] == stream_target_id

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_token_auth_info.yml')
def test_stream_targets_token_auth_info():
    """
    Tests an API call to get the token auth associated with a
    stream target
    """
    response = stream_targets_instance.token_auth_info(stream_target_id)
    assert isinstance(response, dict)
    assert 'token_auth' in response
    assert response['token_auth']['stream_target_id'] == stream_target_id

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_token_auth.yml')
def test_stream_targets_token_auth():
    """
    Tests an API call to get the token auth associated with a 
    particular stream target
    """
    response = stream_targets_instance.token_auth(stream_target_id)
    assert isinstance(response, dict)
    assert 'token_auth' in response
    assert response['token_auth']['stream_target_id'] == stream_target_id

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_token_auth_update.yml')
def test_stream_targets_token_auth_update():
    """
    Tests an API call to update the details associated with a token
    auth for a given stream target
    """
    with pytest.raises(TokenAuthBusy):
        response = stream_targets_instance.update_token_auth(
            stream_target_id,
            {"trusted_shared_secret": "342342E2"}
        )
        assert isinstance(response, dict)
        assert 'TokenAuthBusy' in response['meta']['code']

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_properties_create.yml')
def test_stream_targets_properties_create():
    """
    Tests an API call to create a new property for a given stream target
    """
    response = stream_targets_instance.create_property(
        stream_target_id,
        {
            "section": "hls",
            "key": "chunkSize",
            "value": "6"
        }
    )
    assert isinstance(response, dict)
    assert 'property' in response
    global property_id
    property_id = "{}-{}".format(
        response['property']['section'],
        response['property']['key']
    )

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_properties.yml')
def test_stream_targets_properties():
    """
    Tests an API call to get the properties associated with a particular
    stream target
    """
    response = stream_targets_instance.properties(stream_target_id)
    assert isinstance(response, dict)
    assert 'properties' in response

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_properties_specific.yml')
def test_stream_targets_properties_specific():
    """
    Tests an API call to get a specific stream target property by id
    """
    response = stream_targets_instance.properties(stream_target_id, property_id)
    assert isinstance(response, dict)
    assert 'property' in response

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_properties_delete.yml')
def test_stream_targets_properties_delete():
    """
    Tests an API call to delete a stream target property by id
    """
    response = stream_targets_instance\
        .delete_property(stream_target_id, property_id)
    assert response.status_code == 204

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_geoblock_create.yml')
def test_stream_targets_geoblock_create():
    """
    Tests an API call to create a geoblock for a location
    """
    response = stream_targets_instance.create_geoblock(
        stream_target_id,
        {
            "type": "allow",
            "countries": ["de", "us"],
            "whitelist": "0.0.0.0"
        }
    )
    assert isinstance(response, dict)
    assert 'geoblock' in response
    assert response['geoblock']['stream_target_id'] == stream_target_id

@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_geoblock.yml')
def test_stream_targets_geoblock():
    """
    Tests an API call to get the geoblocks for a given stream target
    """
    response = stream_targets_instance.geoblock(stream_target_id)
    assert isinstance(response, dict)
    assert 'geoblock' in response
    assert response['geoblock']['stream_target_id'] == stream_target_id

# Geoblocking takes too long to set-up for a test, so we don't test
# the update functionality
@vcr.use_cassette('tests/vcr_cassettes/test_stream_targets_geoblock_update.yml')
def test_stream_targets_geoblock_update():
    """
    Tests an API call to update geoblocking details for a stream target
    """
    with pytest.raises(GeoblockingBusy):
        response = stream_targets_instance.update_geoblock(
            stream_target_id,
            {
                "type": "deny",
                "countries": ["hk", "it"],
                "whitelist": "2.2.2.2"
            }
        )
        assert isinstance(response, dict)
        assert 'GeoblockingBusy' in response['meta']['code']


###########
# PLAYERS #
###########

players_instance = Players(
    api_key = WOWZA_API_KEY,
    access_key = WOWZA_ACCESS_KEY
)

@vcr.use_cassette('tests/vcr_cassettes/test_players_info.yml')
def test_players_info():
    """
    Test a GET call to get a player's info
    """
    response = players_instance.info()
    assert isinstance(response, dict)
    assert 'players' in response
    global player_id
    player_id = response['players'][0]['id']

@vcr.use_cassette('tests/vcr_cassettes/test_players_info_specific.yml')
def test_players_info_specific():
    """
    Test a GET call to get a particular player's info by ID
    """
    response = players_instance.info(player_id)
    assert isinstance(response, dict)
    assert response['player']['id'] == player_id

@vcr.use_cassette('tests/vcr_cassettes/test_players_update.yml')
def test_players_update():
    """
    Test a PATCH call to update information associated with
    a particular player
    """
    response = players_instance.update(
        player_id,
        { 'width': '800px' }
    )
    assert isinstance(response, dict)
    assert response['player']['id'] == player_id

@vcr.use_cassette('tests/vcr_cassettes/test_players_state.yml')
def test_players_state():
    """
    Test an API call to get the state of a particular player
    """
    response = players_instance.info(player_id, 'state')
    assert isinstance(response, dict)
    assert 'state' in response['player']

@vcr.use_cassette('tests/vcr_cassettes/test_players_rebuild.yml')
def test_players_rebuild():
    """
    Tests an API call to rebuild a particular player
    """
    response = players_instance.rebuild(player_id)
    assert isinstance(response, dict)
    assert response['player']['state'] in ['requested', 'already_requested'], \
        "The state 'requested' or 'already_requested' should be present in response"

@vcr.use_cassette('tests/vcr_cassettes/test_players_urls_new_missing_params.yml')
def test_players_urls_new_missing_params():
    """
    Tests an API call to create a new URL for a player, but with
    missing required params
    """
    with pytest.raises(MissingParameter):
        response = players_instance.urls(
            player_id=player_id, option='new',
            param_dict = {
                'label': 'intentional failure'
            }
        )
        assert isinstance(response, dict)
        assert 'meta' in response

@vcr.use_cassette('tests/vcr_cassettes/test_players_urls_new.yml')
def test_players_urls_new():
    """
    Tests an API call to create a new URL for a particular player
    """
    response = players_instance.urls(
        player_id=player_id, option='new',
        param_dict = {
            'label': 'Test label',
            'height': 1080,
            'width': 1920,
            'bitrate': 2500,
            'url': 'http://some.url/test/path'
        }
    )
    assert isinstance(response, dict)
    assert 'id' in response['url'], "ID of new URL should be returned in the response"

@vcr.use_cassette('tests/vcr_cassettes/test_players_urls_get.yml')
def test_players_urls_get():
    """
    Tests an API call to get the URLs for a particular player
    """
    response = players_instance.urls(player_id)
    assert isinstance(response, dict)
    global url_ids
    url_ids = [r['id'] for r in response['urls']]

@vcr.use_cassette('tests/vcr_cassettes/test_players_urls_get_specific.yml')
def test_players_urls_get_specific():
    """
    Tests an API call to get details for a specific URL
    """
    response = players_instance.urls(
        player_id=player_id,
        url_id=url_ids[0]
    )
    assert isinstance(response, dict)
    assert 'url' in response

@vcr.use_cassette('tests/vcr_cassettes/test_players_urls_update.yml')
def test_players_urls_update():
    """
    Tests an API call to update the details of a specific URL
    """
    response = players_instance.urls(
        player_id=player_id, url_id=url_ids[0],
        param_dict = {
            'label': 'Test label change'
        }
    )
    assert isinstance(response, dict)
    assert response['url']['id'] == url_ids[0]

@vcr.use_cassette('tests/vcr_cassettes/test_players_urls_delete.yml')
def test_players_urls_delete():
    """
    Tests an API call to delete a specific URL by ID
    """
    for url in url_ids:
        response = players_instance.urls(player_id, 'delete', url)
        assert response.status_code == 204



#############
# RECORDING #
#############

recordings_instance = Recordings(
    api_key=WOWZA_API_KEY,
    access_key=WOWZA_ACCESS_KEY
)

@vcr.use_cassette('tests/vcr_cassettes/test_recordings_get.yml')
def test_recordings_get():
    """
    Tests an API call to get all recordings associated with an account
    """
    response = recordings_instance.info()
    assert isinstance(response, dict)
    assert 'recordings' in response



###############
# TRANSCODERS #
###############

transcoders_instance = Transcoders(
    api_key = WOWZA_API_KEY,
    access_key = WOWZA_ACCESS_KEY
)

@vcr.use_cassette('tests/vcr_cassettes/test_transcoders_create.yml')
def test_transcoders_create():
    """
    Tests an API call to create a transcoder
    """
    trans_data = {
        'name': 'Test Transcoder',
        'transcoder_type': 'transcoded',
        'billing_mode': 'pay_as_you_go',
        'broadcast_location': 'us_east_s_carolina',
        'protocol': 'rtmp',
        'delivery_method': 'push'
    }
    response = transcoders_instance.create(trans_data)
    assert isinstance(response, dict)
    assert 'id' in response['transcoder']
    global trans_id
    trans_id = response['transcoder']['id']

@vcr.use_cassette('tests/vcr_cassettes/test_transcoders_get.yml')
def test_transcoders_get():
    """
    Tests an API call to get all transcoders associated with an account
    """
    response = transcoders_instance.info()
    assert isinstance(response, dict)
    assert 'transcoders' in response


#############
# SCHEDULES #
#############

schedules_instance = Schedules(
    api_key = WOWZA_API_KEY,
    access_key = WOWZA_ACCESS_KEY
)

@vcr.use_cassette('tests/vcr_cassettes/test_schedules_create.yml')
def test_schedules_create():
    """
    Tests an API call to create a new schedule
    """
    response = schedules_instance.create({
        'transcoder_id': trans_id,
        'name': 'Test Schedule',
        'action_type': 'start',
        'begins_at': '2018-01-01T12:00:00.000Z',
        'start_transcoder': '2018-01-01T12:00:00.000Z',
        'recurrence_type': 'once'
    })
    global schedule_id
    schedule_id = response['schedule']['id']
    assert isinstance(response, dict)
    assert 'schedule' in response

@vcr.use_cassette('tests/vcr_cassettes/test_schedules_get.yml')
def test_schedules_get():
    """
    Tests an API call to get all the schedules associated with an account
    """
    response = schedules_instance.info()
    assert isinstance(response, dict)
    assert 'schedules' in response

@vcr.use_cassette('tests/vcr_cassettes/test_schedules_get_state.yml')
def test_schedules_get_state():
    """
    Tests an API call to get the state of a schedule by ID
    """
    response = schedules_instance.info(schedule_id, 'state')
    assert isinstance(response, dict)
    assert 'schedule' in response
    assert 'state' in response['schedule']

@vcr.use_cassette('tests/vcr_cassettes/test_schedules_update.yml')
def test_schedules_update():
    """
    Tests an API call to update the details of a schedule
    """
    response = schedules_instance.update(
        schedule_id,
        {
        'transcoder_id': trans_id,
        'name': 'Test Schedule Name'
        }
    )
    assert isinstance(response, dict)
    assert 'schedule' in response
    assert response['schedule']['id'] == schedule_id

@vcr.use_cassette('tests/vcr_cassettes/test_schedules_disable.yml')
def test_schedules_disable():
    """
    Tests an API call to disable a schedule
    """
    response = schedules_instance.disable(schedule_id)
    assert isinstance(response, dict)
    assert 'schedule' in response
    assert response['schedule']['state'] == 'disabled'

@vcr.use_cassette('tests/vcr_cassettes/test_schedules_enable.yml')
def test_schedules_enable():
    """
    Tests an API call to enable a schedule
    """
    time.sleep(2) # Give wowza time to change the state
    response = schedules_instance.enable(schedule_id)
    assert isinstance(response, dict)
    assert 'schedule' in response
    assert response['schedule']['state'] == 'enabled'

@vcr.use_cassette('tests/vcr_cassettes/test_schedules_toggle.yml')
def test_schedules_toggle():
    """
    Tests an API call to toggle a schedule's active state
    """
    valid_states = ['enabled', 'disabled']
    for _ in range(0, 2): # 2 iterations, to toggle on & off
        current_state = schedules_instance.info(schedule_id, 'state')['schedule']['state']
        assert current_state in valid_states
        time.sleep(2) # Give wowza time to change the state
        response = schedules_instance.toggle(schedule_id)
        assert isinstance(response, dict)
        assert 'schedule' in response
        assert ( (response['schedule']['state'] in valid_states) and \
            (response['schedule']['state'] is not current_state))


###########
# CLEANUP #
###########
@vcr.use_cassette('tests/vcr_cassettes/test_stream_delete.yml')
def test_stream_delete():
    """
    Tests an API call to delete a live stream
    """
    while 1:
        time.sleep(2)
        response = wowza_instance.info(stream_id, 'state')
        print("Response: {}".format(response))
        if response['live_stream']['state'] is not "started":
            response = wowza_instance.delete(stream_id)
            assert response.status_code == 204
            break

@vcr.use_cassette('tests/vcr_cassettes/test_transcoders_delete.yml')
def test_transcoders_delete():
    """
    Tests an API call to delete a transcoder
    """
    response = transcoders_instance.delete(trans_id)
    assert response.status_code == 204
