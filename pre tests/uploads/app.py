#!/usr/bin/python
from flask import Flask, render_template, request
import time
import urllib.parse
app = Flask(__name__)

def convert(input):
    # Converts unicode to string
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, str):
        return input.encode('utf-8')
    else:
        return input

@app.route("/target_endpoint")
def target():
    # You could do any information passing here if you want (i.e Post or Get request)
    some_data = "Here's some example data"
    some_data = urllib.parse.quote(convert(some_data)) # urllib2 is used if you have fancy characters in your data like "+"," ", or "="
    # This is where the loading screen will be.
    # ( You don't have to pass data if you want, but if you do, make sure you have a matching variable in the html i.e {{my_data}} )
    return render_template('loading.html', my_data = some_data)

@app.route("/processing")
def processing():
    # This is where the time-consuming process can be.
    data = "No data was passed"
    # In this case, the data was passed as a get request as you can see at the bottom of the loading.html file
    if request.args.to_dict(flat=False)['data'][0]:
        data = str(request.args.to_dict(flat=False)['data'][0])
    time.sleep(10)
    return render_template('success.html', passed_data = data)

@app.route("/maps")
def maps():
    # import googlemaps
    # from datetime import datetime
    #
    # gmaps = googlemaps.Client(key='AIzaSyC0qHoWIGKA8w6K-UxeXrO_v2G1aeTWwUE')
    #
    # # Geocoding an address
    # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
    #
    # # Look up an address with reverse geocoding
    # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
    #
    # # Request directions via public transit
    # now = datetime.now()
    # directions_result = gmaps.directions("Sydney Town Hall",
    #                                      "Parramatta, NSW",
    #                                      mode="transit",
    #                                      departure_time=now)
    return render_template('maps.html',
                            # directions_result=directions_result,
                            )

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
