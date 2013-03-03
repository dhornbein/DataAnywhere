import sys
import math
import datetime
from bson import ObjectId
from flask import Flask, render_template,request,jsonify

from parse_fields_values import parse_fields_values

sys.path.append('..')
import config

app = Flask(__name__)
app.debug=True

def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
        request.accept_mimetypes[best] > \
        request.accept_mimetypes['text/html']

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/<string:region>/<string:fields_values>',methods=['GET'])
def query_region(region,fields_values):
   
    request_dict = parse_fields_values(fields_values)

    results = [x for x in config.sandy_collection.find(request_dict).limit(50000)]

    for r in results:
        for x,y in r.items():
            if type(y) in (datetime.datetime,ObjectId):
               r[x] = str(y)

    if request_wants_json():
        return jsonify(items=results)

    return jsonify(items=results)
    #return render_template('nonexistent.html', items=items)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    app.run(config.query_f_server,config.query_f_port)
