from flask_cors import CORS
from datetime import datetime
from yelp_query import *
from flask import Flask, render_template, send_from_directory, Response, request, flash, redirect, url_for
from flask_wtf import Form
import flask_wtf
from wtforms import SelectField, DecimalField, BooleanField, SubmitField, StringField, validators, ValidationError
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user , logout_user , current_user , login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


app=Flask(__name__,static_url_path="")
Bootstrap(app)
app.debug=True
app.secret_key = 'jasonhu'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'#'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class SearchForm(Form):
    location = StringField(label="Location",render_kw={'autofocus': True, 'required':True , 'placeholder':'Location'})
    term = StringField(label="Search Term",render_kw={"required":True, 'placeholder':'Search Term'})
    search =SubmitField("Find some restaurants")

class yelpImage():
    imgsrc='yelp_logo.png'
    alt="yelp logo"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(10))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, email , password):
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.username)

db.create_all()


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class MyEqualTo(object):
    """
    Compares the values of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if other.data!="" and field.data != other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('Field must be equal to %(other_name)s.')

            raise ValidationError(message % d)


class LoginForm(Form):
    email = StringField(label="Email",render_kw={"type":"email", 'autofocus': True, 'required':True , 'placeholder':'Email'})
    password = StringField(label="Password",validators=[MyEqualTo('confirm', message='Passwords must match')],render_kw={"type":"password","required":True, 'placeholder':'Password'})
    confirm = StringField(label="Confirm Password",render_kw={"type":"password", 'placeholder':'Confirm password'})
    register = SubmitField("Register or Login")

@app.route("/signin",methods=["GET","POST"])
def login():
    form = LoginForm(request.form, csrf_enabled=False)
    image = yelpImage()
    if request.method == 'POST' and not form.validate():
        flash("Passwords don't match.")
    if request.method == 'POST' and form.validate():
        if form.confirm.data=="":
            # this is a login request
            email = form.email.data
            password = form.password.data
            registered_user = User.query.filter_by(email=email, password=password).first()
            if registered_user is None:
                flash('Username or Password is invalid', 'error')
                return render_template('login.html', form=form, images=[image])
            login_user(registered_user)
            # logged in
            return redirect(request.args.get('next') or url_for('search'))
        else:
            # this is a registration request
            user = User(form.email.data, form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("search"))
            except IntegrityError:
                flash("User exists.")
                db.session.rollback()
            return render_template('login.html', form=form, images=[image])
    return render_template('login.html', form=form, images=[image])

def oldlogin():
    if request.method=='GET':
        image=yelpImage()
        form=LoginForm()
        class SecondaryButton():
            text="hello"
        secondaryButton=SecondaryButton()
        return render_template("login.html",form=form,images=[image],sb=secondaryButton)
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    # flash('User successfully registered')
    # return redirect(url_for('login'))



@app.route("/searchsb")
def searh():
    image=yelpImage()
    form=SearchForm()
    return render_template("searchsb.html",images=[image],form=form)

@app.route("/")
def search():
    image=yelpImage()
    form=SearchForm()
    if form.validate_on_submit():
        print("validated on submit")
    return render_template("search.html",form=form,images=[image])


@app.route("/search")
def oldsearch():
    image=yelpImage()
    form=SearchForm()
    if form.validate_on_submit():
        print("validated on submit")
    return render_template("search.html",form=form,images=[image])

# @app.route('/oldroot')
# # the root should be a search engine that gives an opportunity to log in.
# def oldroot():
#     form=SearchForm()
#     if form.validate_on_submit():
#         countrytable=()
#         return render_template('restaurant.html', countrytable=countrytable,form=form)
#     return render_template('search.html', form=form)

@app.route('/maps',methods=["GET"])
def googlemaps():
    return render_template("googlemaps.html")

@app.route('/example/<path:path>')
def sends_src(path):
    return send_from_directory("example",path)

@app.route("/yelpquery", methods=["GET"])
def query():
    term=request.args.get("term")
    location=request.args.get("location")
    geojson=yelp(term,location)
    if geojson!=None:
        res=Response(geojson)
        res.headers['Content-type'] = 'application/json'
        return res
    else:
        return ('', 204)

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
