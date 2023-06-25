import json
import flask
import timetable.timetable_api_reader as timetable

# Create the flask application
app = flask.Flask(__name__)

# Route for the alerts page (https://127.0.0.1/alerts)
@app.route("/alerts")
def alerts():
    # Get the alerts from the timetable API
    metro_alerts = timetable.get_alerts()
    
    # Return the alerts in reverse order (so the most recent alert is at the top)
    return json.dumps({"alerts": metro_alerts[::-1]})

# Route for the routes page (https://127.0.0.1/route)
@app.route("/route", methods=["POST"])
def routes():
    # Get the response JSON data
    request_data = flask.request.get_json()
    
    # Get the route, wheelchair and aircon data from the response
    route = request_data["route"]
    wheelchair = request_data["wheelchair"]
    aircon = request_data["aircon"]
    
    # Get the bus locations from the timetable API
    bus_locations = timetable.get_bus_location(route, aircon, wheelchair)
    return json.dumps({"busses": bus_locations})

# Route for the index page (https://127.0.0.1/)
@app.route('/')
def index():
    # Return the index.html file when the user renders this page
    return flask.render_template('index.html')

if __name__ == '__main__':
    # Run the flask application
    app.run(host="0.0.0.0", port=8080, debug=False)