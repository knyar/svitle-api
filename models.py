from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import Dict, List

@dataclass_json
@dataclass
class Stream:
    """API response: a single stream."""
    name: str
    url: str

@dataclass_json
@dataclass
class RecentTrack:
    """API response: a single played track."""
    title: str
    start_time: datetime

@dataclass_json
@dataclass
class Station:
    """API response: a single station"""
    current_track: str = ''
    next_track: str = ''
    recent_tracks: List[RecentTrack] = field(default_factory=list)
    streams: List[Stream] = field(default_factory=list)

@dataclass_json
@dataclass
class V2StatusAPIResponse:
    """/v2/status API response."""
    stations: Dict[str, Station]

@dataclass_json
@dataclass
class V1StatusAPIResponse:
    """/v1/status API response."""
    stream_url: str
    flags: str
    current: str = ''
    next: str = ''

@dataclass_json
@dataclass
class StreamInfo:
    """Internal representation of a point-in-time stream information."""
    current_track: str
    next_track: str = ''
    time: datetime = field(default_factory=datetime.now)

# Preferences API

@dataclass_json
@dataclass
class StationConfig:
    """API response: a single station information."""
    id: str
    name: str
    logo: str
    lang: str

@dataclass_json
@dataclass
class Link:
    text: str
    url: str

@dataclass_json
@dataclass
class ContactBlock:
    title: str
    icon_links: List[Link] = field(default_factory=list)
    text_links: List[Link] = field(default_factory=list)

@dataclass_json
@dataclass
class V2PreferencesAPIResponse:
    """/v2/preferences API response."""
    url_support: str
    url_support_ua: str
    url_support_ru: str
    url_archive: str
    url_youtube: str
    stations: List[StationConfig] = field(default_factory=list)
    contacts: List[ContactBlock] = field(default_factory=list)
