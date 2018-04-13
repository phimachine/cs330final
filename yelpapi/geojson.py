import pickle
import json

def make_geojson(response):
    """
    example geojson
    {
        "geometry": {
            "type": "Point",
            "coordinates": [
                -0.145365,
                51.506182
            ]
        },
        "type": "Feature",
        "properties": {
            "category": "patisserie",
            "hours": "10am - 6pm",
            "description": "Modern twists on classic pastries. We're part of a larger chain of patisseries and cafes.",
            "name": "Josie's Patisserie Mayfair",
            "phone": "+44 20 1234 5678"
        }
    },

    :param response: yelp fusion response
    :return: geojson string
    """
    print(type(response))
    # response is a dictionary
    print(response)
    # with open("yelpapi/sample_response","wb") as file:
    #     pickle.dump(response,file)

    json_ret={}
    json_ret["geometry"]={}
    json_ret["geometry"]["type"]="Point"
    coordinates=[response['coordinates']['latitude'],response['coordinates']['longitude']]
    json_ret["geometry"]["coordinates"]=coordinates

    json_ret["type"]="Feature"
    feat={"category": [aliastitle['title'] for aliastitle in response['categories']],
          "phone":response['display_phone'],
          "hours":response['hours'],
          'image_url':response['image_url'],
          'is_claimed':response['is_claimed'],
          'is_closed':response['is_closed'],
          'location':response['location'],
          'name':response['name'],
          'photos':response['photos'],
          'price':response['price'],
          'rating':response['rating'],
          'review_count':response['review_count'],
          'transactions':response['transactions'],
          'url':response['url']
          }
    json_ret["properties"]=feat

    test=json.dumps(json_ret)
    with open("yelpapi/geojson.json",'wb') as file:
        pickle.dump(test,file)
    return json.dumps(json_ret)