import os
from yelpapi.geojson import make_geojson
from yelpapi.query import my_query
import pickle
import json

def yelp(term,location,verbose=False):
    business_id, response=my_query(term,location,verbose)
    geojson=make_geojson(response)
    print(geojson)
    with open("obsolete/example/geojson","wb") as file:
        pickle.dump(geojson,file)
    return geojson