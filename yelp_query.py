import os
from yelpapi.geojson import make_geojson
from yelpapi.query import my_query, NoYelpBusiness
import pickle
import json

def yelp(term,location,verbose=False):
    try:
        business_id, response=my_query(term,location,verbose)
        geojson=make_geojson(response)
        return geojson

    except NoYelpBusiness:
        return None