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
                            url='https://online.svitle.org/fm'),
            models.Stream(name='low',
                            url='https://online.svitle.org/sre'),
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

preferences_response = models.V2PreferencesAPIResponse(
    stations=[
        models.StationConfig(id='svetloe', name='Светлое Радио', logo='svetloe'),
        models.StationConfig(id='svitle', name='Світле Радіо Еммануїл', logo='svitle'),
        models.StationConfig(id='kids', name='Дитяче Світле Радіо', logo='svitle'),
    ],
    url_support='https://svitle.org/ru/partnjorstvo/bankovskie-rekvizity',
    url_archive='https://media.svitle.org/',
    url_youtube='https://www.youtube.com/c/svitleradioEmmanuel/live',
    contacts=[
        models.ContactBlock(
            title='Прямой эфир',
            icon_links=[
                models.Link(text='skype', url='skype:svitleradio?call'),
                models.Link(text='viber', url='viber://chat?number=+380935584412'),
            ],
            text_links=[
                models.Link(text='+38 (044) 383-67-28', url='tel:+380443836728'),
                models.Link(text='+38 (067) 123-75-75', url='tel:+380671237575'),
                models.Link(text='+38 (094) 928-37-28', url='tel:+380949283728'),
            ],
        ),
        models.ContactBlock(
            title='Редакция',
            text_links=[
                models.Link(text='+38 (044) 383-67-28', url='tel:+380443836728'),
                models.Link(text='radio@svitle.org', url='mailto:radio@svitle.org'),
            ],
        ),
        models.ContactBlock(
            title='Бухгалтерия',
            text_links=[
                models.Link(text='+38 (044) 222-67-28', url='tel:+380442226728'),
                models.Link(text='+38 (099) 207-58-22', url='tel:+380992075822'),
            ],
        ),
    ],
)