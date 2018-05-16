from flask_cors import CORS
from yelp_query import *
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g, send_from_directory, Response
from flask_wtf import Form
from wtforms import SelectField, DecimalField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__,static_url_path="")

Bootstrap(app)
app.debug=True
app.secret_key = 'jasonhu'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
db.create_all()


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

#------------------------------------------
# Register & Login with flask-login
#------------------------------------------


class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        try:
            data = User.query.filter_by(username=name, password=passw).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return 'Dont Login'
        except:
            return "Dont Login"


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


if __name__=="__main__":
    app.run(debug=True, port=5001, ssl_context=('cert/server.crt','cert/server.key'))
