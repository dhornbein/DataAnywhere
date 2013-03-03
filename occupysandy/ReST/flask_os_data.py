import sys
import math
import datetime
from bson import ObjectId
from flask import Flask, render_template,request,jsonify

from parse_fields_values import parse_fields_values

#import ../config.py
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

    #search data for request dictionary
    results = [x for x in config.sandy_collection.find(request_dict).limit(50000)]

    #convert date and object ID to string
    for r in results:
        for x,y in r.items():
            if type(y) in (datetime.datetime,ObjectId):
               r[x] = str(y)

    if request_wants_json():
        return jsonify(items=results)

    return jsonify(items=results)
    #return render_template('nonexistent.html', items=items)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/test/<string:fields_values>',methods=['GET'])
def query_region(region,fields_values):
   
    request_dict = parse_fields_values(fields_values)

    #search data for request dictionary
    results = [x for x in config.sandy_collection.find(request_dict).limit(50000)]

    #convert date and object ID to string
    for r in results:
        for x,y in r.items():
            if type(y) in (datetime.datetime,ObjectId):
               r[x] = str(y)

    outbound = []
    for r in results:
        
        structure = {
                'id':r.pop['gid'],
                'timestamp':r.pop['timestamp'],
                'date':r.pop['date'],
                'contact':{
                    'first-name':r.pop['first-name'],
                    'last-name':r.pop['last-name'],
                    'phone':r.pop['phone'],
                    'email':r.pop['email']
                    'contact-lang':r.pop['contact-lang']
                    'contact-origin':r.pop['contact-origin']
                },
                'sandy':{
                    'resident-during-sandy':r.pop['resident-during-sandy'],
                    'city':r.pop['city'],
                    'state':r.pop['state'],
                    'zip':r.pop['zip'],
                },
                'location':{
                    'street':r.pop['street'],
                    'city':r.pop['city'],
                    'state':r.pop['state'],
                    'zip':r.pop['zip'],
                },
                'home':{
                    'occupant-count':r.pop['occupant-count'],
                    'rent-or-own-1':r.pop['rent-or-own-1'],
                    'rent-or-own-2':r.pop['rent-or-own-2'],
                    'resident':r.pop['resident'],
                    'residence-other':r.pop['residence-other'],
                    'have-children':r.pop['have-children'],
                    'have-seniors':r.pop['have-seniors'],
                    'have-disabled':r.pop['have-disabled'],
                    'damage':{
                        'house-has-damage':r.pop['house-has-damage'],
                        'need-help-repair':r.pop['need-help-repair'],
                        'house-has-mold':r.pop['house-has-mold'],
                    }
                }
            }

        structure['other'] = {}
        for x,y in r.items():
            structure['other'][x] = y
        
        outbound.append(structure)


    if request_wants_json():
        return jsonify(items=outbound)

    return jsonify(items=results)
    #return render_template('nonexistent.html', items=items)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    app.run(config.query_f_server,config.query_f_port)
