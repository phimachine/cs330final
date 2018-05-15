from flask_cors import CORS
from yelp_query import *
from flask import Flask, render_template, send_from_directory, Response, request
from flask_wtf import Form
from wtforms import SelectField, DecimalField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app=Flask(__name__,static_url_path="")
Bootstrap(app)
app.debug=True
app.secret_key = 'jasonhu'

class SearchForm(Form):
    location = StringField(label="Location",render_kw={'autofocus': True, 'required':True , 'placeholder':'Location'})
    term = StringField(label="Search Term",render_kw={"required":True, 'placeholder':'Search Term'})
    submit =SubmitField("Find some restaurants")

class LoginForm(Form):
    email = StringField(label="Email",render_kw={"type":"email", 'autofocus': True, 'required':True , 'placeholder':'Location'})
    password = StringField(label="Password",render_kw={"type":"password","required":True, 'placeholder':'Search Term'})
    register = SubmitField("Register")
    login= SubmitField("Login")

class yelpImage():
    imgsrc='yelp_logo.png'
    alt="yelp logo"

@app.route("/")
def login():
    image=yelpImage()
    form=LoginForm()
    class SecondaryButton():
        text="hello"
    secondaryButton=SecondaryButton()
    return render_template("login.html",form=form,images=[image],sb=secondaryButton)

@app.route("/search")
def search():
    image=yelpImage()
    form=SearchForm()
    return render_template("search.html",form=form,images=[image])

# @app.route('/oldroot')
# # the root should be a search engine that gives an opportunity to log in.
# def oldroot():
#     form=SearchForm()
#     if form.validate_on_submit():
#         countrytable=()
#         return render_template('restaurant.html', countrytable=countrytable,form=form)
#     return render_template('search.html', form=form)

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
