import json
import flask

import timetable_api_reader as timetable

app = flask.Flask(__name__)

@app.route("/alerts")
def alerts():
    metro_alerts = timetable.get_alerts()
    return json.dumps({"alerts": metro_alerts[::-1]})

@app.route("/route", methods=["POST"])
def routes():
    request_data = flask.request.get_json()
    
    route = request_data["route"]
    wheelchair = request_data["wheelchair"]
    aircon = request_data["aircon"]
    
    bus_locations = timetable.get_bus_location(route, aircon, wheelchair)
    return json.dumps({"busses": bus_locations})

@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)