# wowza.py

-----

wowza.py is an API wrapper for Wowza Streaming Cloud REST API written in Python.

This was written to enable the use of the Wowza Streaming Cloud REST API with the Python programming language. Familiarise yourself with their API using their [documentation](https://sandbox.cloud.wowza.com/apidocs/v1/#).

## Installing

-----

To install the library, you can install from source or you can install using pip:

Using pip:

``` pip3 install wowza```

Installing from source:

```bash
git clone https://github.com/atlusio/wowza
cd wowza
python3 setup.py install
```

# Usage

-----

Export your API/Access keys as environment variables:

```
export WOWZA_API_KEY = 'abcdefghijklmnopqrstuvwxyz1234567890'
export WOWZA_ACCESS_KEY = '0987654321zyxwvytsrqonmkjihgfedcba'
```

Import the desired object into the code, and instantiate it with the API/Access keys:

```python
from wowza import LiveStreams, WOWZA_API_KEY, WOWZA_ACCESS_KEY
# Instantiate a LiveStreams instance
wowza_instance = LiveStreams(
    api_key = WOWZA_API_KEY,
    access_key = WOWZA_ACCESS_KEY
)
```

*Note: Default production level is sandbox. Set production level to PROD to hit the production-level API endpoints.*

```bash
export WOWZA_PRODUCTION_LEVEL='PROD'
```

# Quick Example

-----

```python
from wowza import LiveStreams, WOWZA_API_KEY, WOWZA_ACCESS_KEY

# Instantiate a LiveStreams instance
response = wowza_instance = LiveStreams(
    api_key = WOWZA_API_KEY,
    access_key = WOWZA_ACCESS_KEY
)
stream_id = response['live_stream']['id']
# Create a Live Stream
wowza_instance.create({
    'name': 'Test1',
    'broadcast_location': 'us_east_s_carolina',
    'encoder': 'wowza_gocoder',
    'aspect_ratio_width': 1280,
    'aspect_ratio_height': 720
})

# Create a StreamTargets instance
stream_targets_instance = StreamTargets(
    api_key = WOWZA_API_KEY,
    access_key = WOWZA_ACCESS_KEY
)
# Create a stream target
response = stream_targets_instance.create({
    'name': 'Test Stream Target Wowza',
    'type': 'WowzaStreamTarget',
    'location': 'us_west_california'
})
stream_target_id = response['stream_target']['id']

# Geoblock the stream target to certain regions
stream_targets_instance.create_geoblock(
    stream_target_id,
    {
        "type": "allow",
        "countries": ["de", "us"],
        "whitelist": "0.0.0.0"
    }
)

# Start the stream
wowza_instance.start(stream_id)
```

# Requirements

-----

- Python 3.6+
- `requests` library
- `pytest` library
- `vcrpy` library

# License

-----

This Python wrapper distributed under the [MIT License](master/LICENSE.txt)

Wowza and Wowza Streaming Engine is a trademark of Wowza Media Systems™. 