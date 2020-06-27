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
            models.Stream(
                name='default',
                url='https://online.svitle.org/hls/svitle/default.m3u8'),
            models.Stream(
                name='low',
                url='https://online.svitle.org/hls/svitle/low.m3u8'),
        ]
    ),
    'svetloe': models.Station(
        streams=[
            models.Stream(
                name='default',
                url='https://online.svitle.org/hls/svetloe/default.m3u8'),
            models.Stream(
                name='low',
                url='https://online.svitle.org/hls/svetloe/low.m3u8'),
        ]
    ),
    'kids': models.Station(
        streams=[
            models.Stream(
                name='default',
                url='https://online.svitle.org/hls/kids/default.m3u8'),
            models.Stream(
                name='low',
                url='https://online.svitle.org/hls/kids/low.m3u8'),
        ]
    ),
}

v1_response = models.V1StatusAPIResponse(
    stream_url='http://online.svitle.org:6728/sre',  # 64Kbit/s mono'
    # http://online.svitle.org:6728/fm',  # 128Kbit/s stereo
    flags='redirect-obsolete',
)

preferences_svitle_response = models.V2PreferencesAPIResponse(
    stations=[
        models.StationConfig(id='svitle', name='Світле Радіо Еммануїл', logo='svitle'),
        models.StationConfig(id='svetloe', name='Светлое Радио', logo='svetloe'),
        models.StationConfig(id='kids', name='Дитяче Світле Радіо', logo='kids'),
    ],
    url_support='https://svitle.org/ru/partnjorstvo/bankovskie-rekvizity',
    url_archive='https://media.svitle.org/',
    url_youtube='https://www.youtube.com/c/svitleradioEmmanuel/live',
    contacts=[
        models.ContactBlock(
            title='contacts_screen.block.svitle',
            text_links=[
                models.Link(text='svitle.org', url='https://www.svitle.org'),
            ],
        ),
        models.ContactBlock(
            title='contacts_screen.block.live',
            icon_links=[
                models.Link(text='skype', url='skype:svitleradio?chat'),
                models.Link(text='viber', url='viber://chat?number=+380935584412'),
            ],
            text_links=[
                models.Link(text='+38 (067) 123-75-75', url='tel:+380671237575'),
                models.Link(text='+38 (094) 928-37-28', url='tel:+380949283728'),
                models.Link(text='facebook.com/svitleradio', url='https://www.facebook.com/svitleradio'),
            ],
        ),
        models.ContactBlock(
            title='contacts_screen.block.editors',
            text_links=[
                models.Link(text='+38 (044) 221-54-20', url='tel:+380442215420'),
                models.Link(text='radio@svitle.org', url='mailto:radio@svitle.org'),
            ],
        ),
        models.ContactBlock(
            title='contacts_screen.block.accounting',
            text_links=[
                models.Link(text='+38 (099) 207-58-22', url='tel:+380992075822'),
            ],
        ),
        models.ContactBlock(
            title='contacts_screen.block.svetloe',
            text_links=[
                models.Link(text='svetloe.org', url='https://www.svetloe.org'),
            ],
        ),
    ],
)
