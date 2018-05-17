from datetime import datetime
from yelp_query import *
from flask import Flask, render_template, send_from_directory, Response, request, flash, redirect, url_for, g, session
from flask_wtf import Form
from wtforms import SelectField, DecimalField, BooleanField, SubmitField, StringField, validators, ValidationError
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user , logout_user , current_user , login_required, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from yelpapi.geojson import getFeat
import json

class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.username = 'Guest'
app=Flask(__name__,static_url_path="")
Bootstrap(app)
app.debug=True
app.secret_key = 'jasonhu'
login_manager = LoginManager()
login_manager.anonymous_user = Anonymous

login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'#'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

theusername=None

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
    password = db.Column('password', db.String(10))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, email , password):
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
        self.is_authenticated=True
        self.is_anonymous=False

    def is_authenticated(self):
        return self.is_authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.username)

restcat = db.Table('restcat',
    db.Column('restaurant', db.String(50), db.ForeignKey('restaurants.id'), primary_key=True, index=True),
    db.Column('category', db.Integer, db.ForeignKey('restaurant_categories.id'), primary_key=True, index=True)
)

class Restaurant(db.Model):
    __tablename__= 'restaurants'
    id= db.Column(db.String(50),primary_key=True)
    name = db.Column('name', db.String(50),nullable=False)
    categories=db.relationship('RestaurantCategoy',secondary=restcat, lazy='subquery',backref=db.backref('restaurants', lazy=True))
    phone= db.Column('phone',db.String(20))
    image_url=db.Column('image_url',db.String(300))
    location_id=db.Column(db.Integer,db.ForeignKey("locations.id"),nullable=False)
    location=db.relationship('Location',backref=db.backref('restaurants',lazy=True))
    # location=db.relationship("Location",backref=db.backref("restaurants",lazy=True))
    price=db.Column('price',db.String(10))
    rating=db.Column('rating',db.Float)
    review_count=db.Column('review_count',db.Integer)
    url=db.Column('url',db.String(300))

class RestaurantCategoy(db.Model):
    __tablename__='restaurant_categories'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(40),unique=True)

class Location(db.Model):
    __tablename__= 'locations'
    id = db.Column(db.Integer, primary_key=True)
    # restaurant_id = db.Column(db.String(50), db.ForeignKey('restaurants.id'),
    #     nullable=False)
    # restaurant_id=db.relationship("Restaurant",backref=db.backref("locations",lazy=True))

    address1=db.Column(db.String(100), nullable=False)
    address2=db.Column(db.String(100), nullable=False)
    address3=db.Column(db.String(100), nullable=False)
    city=db.Column(db.String(100), nullable=False)
    zip_code=db.Column(db.String(100), nullable=False)
    country=db.Column(db.String(100), nullable=False)
    state=db.Column(db.String(100), nullable=False)

class Interest(db.Model):
    __tablename__='interests'
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.user_id"),nullable=False)
    user = db.relationship('User',backref=db.backref('interests',lazy=True))
    restaurant_id=db.Column(db.String(50),db.ForeignKey("restaurants.id"),nullable=False)
    restaurant=db.relationship('Restaurant',backref=db.backref('interests',lazy=True))
    count=('count',db.Integer)

db.session.flush()
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

@app.route("/restaurantinfo",methods=["GET"])
def restaurantinfo():
    id=request.args.get("id")
    rest=Restaurant.query.filter_by(id=id).first()
    to_json={}
    cat_string=""
    for cat in rest.categories:
        cat_string+=cat.name
        cat_string+="\\"
    cat_string=cat_string[:-1]
    to_json["category"]=[i.name for i in rest.categories]
    to_json["image_url"]=rest.image_url
    loc=rest.location
    addr_list=[loc.address1,loc.address2,loc.address3,loc.city,loc.state,loc.country,loc.zip_code]
    addr_list=[i for i in addr_list if i!=""]
    location_string=', '.join(addr_list)
    to_json["location_string"]=location_string
    to_json["location"]=addr_list
    to_json["name"]=rest.name

    res = Response(json.dumps(to_json))
    res.headers['Content-type'] = 'application/json'
    return res

@app.route("/spy",methods=["POST"])
@login_required
def spy():
    print(g.user)


    return None

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
            if g.user.email!=None:
                theusername=g.user.email
            return redirect(url_for('search'))
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
    geojson, businessid, response=yelpid(term,location)

    if geojson!=None:
        # enter the restaurant information in the database
        foundRest=Restaurant.query.filter_by(id=businessid).first()
        if foundRest is None:

            rest=Restaurant(id=businessid,name=getFeat("name",response),phone=getFeat('phone',response),
                            image_url=getFeat('image_url',response),price=getFeat("price",response),
                            rating=getFeat("rating",response),review_count=getFeat("review_count",response),
                            url=getFeat("url",response))

            categories=getFeat("category",response)
            for cat in categories:
                foundCat=RestaurantCategoy.query.filter_by(name=cat).first()
                if foundCat is None:
                    newcat = RestaurantCategoy(name=cat)
                    try:
                        db.session.add(newcat)
                        db.session.commit()
                    except:
                        db.session.rollback()
                        raise
                    rest.categories.append(newcat)
                else:
                    rest.categories.append(foundCat)

            location=getFeat("location",response)
            address1=location['address1']
            address2=location['address2']
            address3=location['address3']
            city=location['city']
            zip_code=location['zip_code']
            country=location['country']
            state=location['state']
            db.session.rollback()
            foundLoc=Location.query.filter_by(address1=address1,address2=address2,address3=address3,
                                              city=city,zip_code=zip_code,country=country,state=state).first()
            if foundLoc is None:
                newloc=Location(address1=address1,address2=address2,address3=address3,
                                              city=city,zip_code=zip_code,country=country,state=state)
                rest.location=newloc

                db.session.add(newloc)

            db.session.add(rest)
            db.session.commit()

        res=Response(geojson)
        res.headers['Content-type'] = 'application/json'
        return res
    else:
        return ('', 204)

@app.before_request
def before_request():
    g.user = current_user

@app.route("/userinfo",methods=["GET"])
@login_required
def userinfo():
    request.args.get('restid')
    return redirect(url_for('search'))

@app.route("/spaa",methods=["GET"])
@login_required
def userinfao():
    request.args.get('restid')
    return redirect(url_for('search'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('search'))

@app.route("/yelpqueryold", methods=["GET"])
def oldquery():
    term = request.args.get("term")
    location = request.args.get("location")
    geojson = yelp(term, location)
    if geojson != None:
        res = Response(geojson)
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
