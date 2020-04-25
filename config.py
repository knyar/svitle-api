import models

icecast_url = 'https://online.svitle.org/status-json.xsl'

# Convert from legacy names into more readable ones.
stream_name_overrides = {
    'fm': 'svitle-128-aac',
    'sre': 'svitle-64-mp3',
}

redis_key_prefix = 'svitle'

stations = {
    'svitle': models.Station(
        streams=[
            models.Stream(name='normal',
                            url='https://online.svitle.org/sre'),
            models.Stream(name='low',
                            url='https://online.svitle.org/fm'),
        ]
    ),
    'svetloe': models.Station(
        streams=[
            models.Stream(
                name='normal',
                url='https://online.svitle.org/svetloe.128.mp3'),
        ]
    ),
    'kids': models.Station(
        streams=[
            models.Stream(
                name='normal',
                url='https://online.svitle.org/kids.128.mp3'),
        ]
    ),
}

v1_response = models.V1StatusAPIResponse(
    stream_url='http://online.svitle.org:6728/sre',  # 64Kbit/s mono'
    # http://online.svitle.org:6728/fm',  # 128Kbit/s stereo
    flags='redirect-obsolete',
)