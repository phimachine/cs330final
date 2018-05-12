from flask_cors import CORS
from yelp_query import *
from flask import Flask, render_template, send_from_directory, Response, request
from flask_wtf import Form
from wtforms import SelectField, DecimalField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import query

app=Flask(__name__,static_url_path="")
Bootstrap(app)
app.debug=True
app.secret_key = 'jasonhu'

class searchForm(Form):
    location = StringField(label="Location")
    term = StringField("Search Term")
    submit =SubmitField("Find some restaurants")

@app.route('/')
# the root should be a search engine that gives an opportunity to log in.
def root():
    form=searchForm()
    if form.validate_on_submit():
        countrytable=()
        return render_template('restaurant.html', countrytable=countrytable,form=form)
    return render_template('testsearch.html', form=form)

@app.route('/googlemaps')
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

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory("css",path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory("img",path)

if __name__=="__main__":
    app.run(debug=True, port=5001, ssl_context=('cert/server.crt','cert/server.key'))
