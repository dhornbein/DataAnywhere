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

@app.route('/1/<string:region>/<string:fields_values>',methods=['GET'])
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

@app.route('/2/<string:fields_values>',methods=['GET'])
def query_structure(fields_values):
   
    request_dict = parse_fields_values(fields_values)

    #search data for request dictionary
    results = [x for x in config.sandy_collection.find(request_dict).limit(50000)]
        
    outbound = []

    #convert date and object ID to string
    for r in results:
        for x,y in r.items():
            if type(y) in (datetime.datetime,ObjectId):
               r[x] = str(y)

        
        structure = {
                'id':r.pop('gid',None),
                'timestamp':r.pop('timestamp',None),
                'date':r.pop('date',None),
                'contact':{
                    'first-name':r.pop('first-name',None),
                    'last-name':r.pop('last-name',None),
                    'phone':r.pop('phone',None),
                    'email':r.pop('email',None),
                    'contact-lang':r.pop('contact-lang',None),
                    'contact-origin':r.pop('contact-origin',None)
                },
                'sandy':{
                    'resident-during-sandy':r.pop('resident-during-sandy',None)
                },
                'location':{
                    'street':r.pop('street',None),
                    'city':r.pop('city',None),
                    'state':r.pop('state',None)
                },
                'home':{
                    'occupant-count':r.pop('occupant-count',None),
                    'rent-or-own-1':r.pop('rent-or-own-1',None),
                    'rent-or-own-2':r.pop('rent-or-own-2',None),
                    'resident':r.pop('resident',None),
                    'residence-other':r.pop('residence-other',None),
                    'have-children':r.pop('have-children',None),
                    'have-seniors':r.pop('have-seniors',None),
                    'have-disabled':r.pop('have-disabled',None),
                    'damage':{
                        'house-has-damage':r.pop('house-has-damage',None),
                        'need-help-repair':r.pop('need-help-repair',None),
                        'house-has-mold':r.pop('house-has-mold',None)
                    }
                }
            }

        structure['other'] = {}
        for x,y in r.items():
            structure['other'][x] = y
       
	# Remove None values 
	structure.update((k, v) for k, v in structure.iteritems() if v is not None)

        outbound.append(structure)


    if request_wants_json():
        return jsonify(items=outbound)

    return jsonify(items=outbound)
    #return render_template('nonexistent.html', items=items)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    app.run(config.query_f_server,config.query_f_port)
