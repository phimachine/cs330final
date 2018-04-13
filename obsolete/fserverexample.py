from flask import Flask, Response, request, send_from_directory
import random, json
from pathlib import Path
import os


app=Flask(__name__, static_url_path='')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/')
def _3():
    return send_from_directory('',"shopping.html")


# @app.route('/getshoppinglist')
# def _():
#     with open("shoppingList.json", "rb") as datafile:
#         # raw=json.load(datafile)
#         raw=datafile.read()
#         res=Response(raw)
#         res.headers['Content-type'] = 'application/json'
#         return res

# @app.route('/shoppinglist',methods=['GET','POST'])
# def _2():
#     if request.method=='GET':
#         with open("shoppingList.json", "r") as datafile:
#             # raw=json.load(datafile)
#             raw=json.load(datafile)
#             res=Response(raw)
#             res.headers['Content-type'] = 'application/json'
#     else:
#         with open("shoppingList.json", "w") as datafile:
#             # json.dump(raw, datafile)
#             res=request.data
#             json.dump(res,datafile)
#     return res


@app.route('/shoppinglist',methods=['GET','POST'])
def _2():
    # print(os.getcwd())
    # print(os.path.dirname(os.path.realpath(__file__)))
    wd=os.path.dirname(os.path.realpath(__file__))

    # test working directory again
    filedir=wd+"/shoppingList.json"
    my_file = Path(filedir)

    # if my_file.is_file():
    #     print(filedir+ ": file not found")
    # else:
    #     print(filedir+": file found")

    if request.method=='GET':
        print(request.method)
        with open(filedir,  "rb") as datafile:
            # raw=json.load(datafile)
            raw=datafile.read()
            res=Response(raw)
            res.headers['Content-type'] = 'application/json'
        return res
    else:
        print(request.method)
        with open(filedir, "wb") as datafile:
            # json.dump(raw, datafile)
            res=request.data
            datafile.write(res)
        return res

    # raw=request.data
    # with open("shoppingList.json", "wb") as datafile:
    #     # json.dump(raw, datafile)
    #     datafile.write(raw)
    #     return None

@app.route('/shoppinglistauto', methods=['GET', 'POST'])
def _auto():
    # print(os.getcwd())
    # print(os.path.dirname(os.path.realpath(__file__)))
    wd = os.path.dirname(os.path.realpath(__file__))

    # test working directory again
    filedir = wd + "/shoppingListAuto.json"
    my_file = Path(filedir)

    # if my_file.is_file():
    #     print(filedir+ ": file not found")
    # else:
    #     print(filedir+": file found")

    if request.method == 'GET':
        if os.path.exists(filedir):
            print(request.method)
            with open(filedir, "rb") as datafile:
                # raw=json.load(datafile)
                raw = datafile.read()
                res = Response(raw)
                res.headers['Content-type'] = 'application/json'
            return res
    else:
        print(request.method)
        with open(filedir, "wb") as datafile:
            # json.dump(raw, datafile)
            res = request.data
            datafile.write(res)
        return res

    # raw=request.data
    # with open("shoppingList.json", "wb") as datafile:
    #     # json.dump(raw, datafile)
    #     datafile.write(raw)
    #     return None


if __name__=="__main__":
    app.run(debug=True, port=5001)
