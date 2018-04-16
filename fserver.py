from flask import Flask, Response, send_from_directory, request
from flask_cors import CORS
from yelp_query import *

app=Flask(__name__,static_url_path="")
cors=CORS(app)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory("css",path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory("img",path)

@app.route('/')
def root():
    return send_from_directory('',"search.html")

@app.route('/googlemaps.html')
def googlemaps():
    return send_from_directory("","googlemaps.html")

@app.route('/example/<path:path>')
def sends_src(path):
    return send_from_directory("example",path)

@app.route("/yelpquery")
def query():
    term=request.args.get("term")
    location=request.args.get("location")
    geojson=yelp(term,location)
    res=Response(geojson)
    res.headers['Content-type'] = 'application/json'
    return res


# ?term="+term+"&location="+location)



if __name__=="__main__":
    app.run(debug=True, port=5001, ssl_context=('cert/server.crt','cert/server.key'))