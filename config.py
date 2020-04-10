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
