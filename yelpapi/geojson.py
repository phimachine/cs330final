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
    # print(type(response))
    # response is a dictionary
    # print(response)
    # with open("yelpapi/sample_response","wb") as file:
    #     pickle.dump(response,file)

    json_ret={}
    json_ret["geometry"]={}
    json_ret["geometry"]["type"]="Point"
    coordinates=getFeat("coor",response)
    json_ret["geometry"]["coordinates"]=coordinates

    json_ret["type"]="Feature"
    feat={"category": getFeat("category",response),
          "phone":getFeat("phone",response),
          "hours":getFeat("hours",response),
          'image_url':getFeat("image_url",response),
          'is_claimed':getFeat("is_claimed",response),
          'is_closed':getFeat("is_closed",response),
          'location':getFeat("location",response),
          'name':getFeat("name",response),
          'photos':getFeat("photo",response),
          'price':getFeat("price",response),
          'rating':getFeat("rating",response),
          'review_count':getFeat("review_count",response),
          'transactions':getFeat("transactions",response),
          'url':getFeat("url",response)
          }
    json_ret["properties"]=feat

    # test=json.dumps(json_ret)
    # with open("yelpapi/geojson.json",'wb') as file:
    #     pickle.dump(test,file)
    return json.dumps(json_ret)

def getFeat(mykey, response):
    try:
        if mykey=="category":
            return [aliastitle['title'] for aliastitle in response['categories']]
        elif mykey=="phone":
            return response['display_phone']
        elif mykey=="coor":
            return [response['coordinates']['longitude'],response['coordinates']['latitude']]
        else:
            return response[mykey]
    except KeyError:
        return None


def getgeojsonid(response):
    json_ret={}
    json_ret["geometry"]={}
    json_ret["geometry"]["type"]="Point"
    coordinates=getFeat("coor",response)
    json_ret["geometry"]["coordinates"]=coordinates
    json_ret["type"]="Feature"
    feat={"id": getFeat("id",response)}
    json_ret["properties"]=feat
    return json.dumps(json_ret)

