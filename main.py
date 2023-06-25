import json
import flask

import timetable_api_reader as timetable

app = flask.Flask(__name__)

@app.route("/alerts")
def alerts():
    sample_json = {
        "alerts": [
            {
                "title": "Alert 1",
                "content": "This is the first alert"
            },
            {
                "title": "Alert poo",
                "content": "asdfdsa fadlk;dsfl;kdsalfnsf;ldn;k jdf;k ;k  kfd lksfdg lkl"
            }
        ]
    }
    return json.dumps(sample_json)

@app.route("/route", methods=["POST"])
def routes():
    request_data = flask.request.get_json()
    
    # Get the route shit here
    
    sample_json = {
        "busses": [
            {
                "latitude": "-34.924164070184126",
                "longitude": "138.60093358259886"
            },
            {
                "latitude": "-34.824164070184126",
                "longitude": "138.60093358259886"
            }
        ]
    }
    print("Route request")
    
    return json.dumps(sample_json)

@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)