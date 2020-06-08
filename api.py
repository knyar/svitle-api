import copy

from flask import current_app as app
from flask import jsonify, request, Response
from flask_restful import Api, Resource

import config
import models

class V2Status(Resource):
    """Request handler for /v2/status.

   Accepts the following GET parameters:
    - recent_tracks: if set to 0, recent track information will not be
      included.
    - station: if set, only the specified station will be included in
      the response. Can be specified multiple times.

    Returns a response message in models.V2StatusAPIResponse
    """
    def get(self):
        stations = copy.deepcopy(config.stations)
        arg_station = request.args.getlist('station')
        if arg_station:
            stations = {n: s for n, s in stations.items()
                        if n in arg_station}

        arg_recent_tracks = request.args.get(
            'recent_tracks', default=1, type=int)
        fetcher_stations = app.sv_fetcher.stations
        for name, stream_info in fetcher_stations.items():
            if name not in stations:
                continue
            stations[name].current_track = stream_info.current_track
            stations[name].next_track = stream_info.next_track
            if arg_recent_tracks == 0:
                continue
            for stream_info in app.sv_store.get_history(name):
                stations[name].recent_tracks.append(
                    models.RecentTrack(
                        title=stream_info.current_track,
                        start_time=stream_info.time,
                    ))

        resp = models.V2StatusAPIResponse(stations=stations)
        return Response(
            resp.to_json(), 200, mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'})


class V2Preferences(Resource):
    """Request handler for /v2/preferences.

    Returns a response message in models.V2PreferencesResponse
    """
    def get(self):
        return Response(
            config.preferences_response.to_json(), 200, mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'})


class V1Status(Resource):
    """Request handler for /v1/status.

    Returns a response message in models.V1StatusAPIResponse
    """
    def get(self):
        response = copy.deepcopy(config.v1_response)
        svitle = app.sv_fetcher.stations['svitle']
        response.current = svitle.current_track
        response.next = svitle.next_track
        return Response(
            response.to_json(), 200, mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'})


api = Api()
api.add_resource(V2Status, '/v2/status')
api.add_resource(V2Preferences, '/v2/preferences')
api.add_resource(V1Status, '/v1/status')
