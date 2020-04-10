import copy

from flask import current_app as app
from flask import jsonify, Response
from flask_restful import Api, Resource

import config
import models

class V2Status(Resource):
    def get(self):
        stations = copy.deepcopy(config.stations)
        fetcher_stations = app.sv_fetcher.stations
        for name, stream_info in fetcher_stations.items():
            stations[name].current_track = stream_info.current_track
            stations[name].next_track = stream_info.next_track
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


api = Api()
api.add_resource(V2Status, '/v2/status')
