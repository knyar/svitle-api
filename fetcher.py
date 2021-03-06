import json
import logging
import requests
import threading
import time
from typing import Dict

from prometheus_client.core import GaugeMetricFamily

import config
import models

_SEPARATOR = r'=›Next=›'

class Fetcher(object):
    def __init__(self, store):
        """Initialize the fetcher object, start background refresh."""
        self._store = store
        self.listener_counts = {} # stream name -> listener count
        self.stations = {} # station name -> StreamInfo

        for station in config.stations.keys():
            history = self._store.get_history(station, 1)
            if history:
                self.stations[station] = history[0]

        logging.info("Starting the fetcher thread")
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

    def _run(self):
        """Background refresh function that runs in a loop."""
        while True:
            try:
                sources = _fetch_sources()
                logging.debug("Fetched %d sources", len(sources))
                self._process_sources(sources)
                logging.debug("Stations: %s", self.stations)
                logging.debug("Listener counts: %s", self.listener_counts)
            except Exception as e:
                logging.error("Fetcher error: %s", e)
            time.sleep(1)

    def _process_sources(self, sources: Dict[str, object]):
        """Process fetched source information, update exported data."""
        stations = {}
        listener_counts = {}
        for name, source in sources.items():
            listener_counts[name] = int(source.get('listeners', 0))
            station = self.stream_to_station(name)
            if not station or station in stations:
                continue
            stream_info = _parse_stream_info(name, source)
            stations[station] = stream_info

            if ((station in self.stations) and
                    (self.stations[station].current_track ==
                    stream_info.current_track)):
                continue
            if stream_info.current_track == '':
                continue
            logging.debug("Adding new stream information for %s", station)
            self._store.add_stream_info(station, stream_info)
        self.stations = stations
        self.listener_counts = listener_counts

    def stream_to_station(self, stream: str) -> str:
        for station in config.stations.keys():
            if stream.startswith(station):
                return station
        return None

    def collect(self):
        """Prometheus metric collection function.

        This must be called 'collect'.
        """
        updated = 0
        streams = self.stations
        if len(streams) > 0:
            updated = next(iter(streams.values())).time.timestamp()
        yield GaugeMetricFamily(
            'svitlelistener_updated', 'Last update timestamp', value=updated)

        l = GaugeMetricFamily(
            'svitlelistener_count', 'Number of listeners', labels=['type'])
        for name, count in self.listener_counts.items():
            l.add_metric([name], count)
        yield l


def _parse_stream_info(name: str, source: object) -> models.StreamInfo:
    """Parse a StreamInfo model from an icecast source object."""
    if 'title' not in source:
        return models.StreamInfo(current_track='', next_track='')
    title = source['title']

    # Sometimes stream titles have this in their name :(
    title = title.replace('?UNKNOWN?', '')

    # A separator might be used to separate current and next tracks.
    parts = title.split(_SEPARATOR)

    return models.StreamInfo(
        current_track=_strip(parts[0]),
        next_track=_strip(parts[1]) if len(parts) > 1 else '',
    )

def _strip(input: str) -> str:
    """Strip whitespace and other junk characters."""
    return input.strip(" \t\n\r\0\x0B.,;-")

def _fetch_sources() -> Dict[str, object]:
    """Fetch sources currently active in icecast.

    Returns a dict with keys corresponding to normalized source
    names.
    """
    r = requests.get(config.icecast_url, timeout=10)

    # Sometimes icecast2 returnes invalid JSON when the title is empty :(
    # The fix is in master but the released version (2.4.4) does not
    # include it yet. https://trac.xiph.org/ticket/2198
    text = r.text.replace('"title": - ,', '"title": "",')
    data = json.loads(text)
    sources = data['icestats']['source']

    if not isinstance(sources, list):
        sources = [sources]

    r = {}
    for source in sources:
        name = source['listenurl'].split('/')[-1]
        name = config.stream_name_overrides.get(name, name.replace('.', '-'))
        r[name] = source
    return r
