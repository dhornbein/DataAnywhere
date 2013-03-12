---
layout: home
title: Home
---

## Background

The {{ site.projectname }} project was developed at the [#OccupyDataNYC Hackathon][1] on March 1st & 2nd. Read the [project outline][2]. It is currently being tested for use with Hurricane Sandy relief around New York City as part of [#OccupySandy][3].

### The problem

There are many relief and rebuilding focused organizations collecting data. This data needs to be both **shared with collaborators** and **secure, to protect private information**.

Currently data is stored in many (mainly proprietary) software packages, if it is even digitized at all. Data stewards don't have good ways to share public data while keeping private data secure. 

You can read more about this project on [Drew's Blog post][4].

## Solution

{{ site.projectname }} seeks to provide a simple, extend-able, single focus solution to storing, securing, and sharing any kind of data.

Here's a vague diagram outlining the collection of paper forms:  
![{{ site.projectname }} diagram](http://blog.dhornbein.com/wp-content/uploads/2013/03/dataanywhere_workflow_draf1.png)

1. Data is collected with a form based on community needs and collective data standards.
2. Data is entered into a computer, digitized. If information is collected digitally this step is simplified.
3. Data is mapped to a standardized format for storage. Structuring input data to match standards will simplify this process.
4. Data is stored in an off-the-shelf server.
5. A data API is developed to manipulate stored data. Data stewards control how data is made available. By following collective standards uniform data can be distributed to a network of data servers.
6. App authors can access shared data from the server network to run services.
7. Apps can interface with other systems both open and closed.

# [The System Set up](./setup.html)

{{ site.projectname }} can be broken down into three distinct sections:

1. **[Server Setup](./server_setup.html)** - Data stewards will need to configure a VPS (virtual private server)
2. **[Data Import](./data_import.html)** - Taking non standard data from bizarre sources (initially with a focus on `.csv`) and import them into a **standardized** MongoDB data structure.
3. **[RESTful API development](./restful_api)** - Using Python with Flask simple standardized API will need to be customized depending on the data.

Each step will initially be very hands on. As standards are developed common libraries can be created to manage each step.

## [Server Setup](./server_setup.html)

The current strategy is to set up an off-the-shelf VPS server running either Ubuntu or Fedora.

The stack:
* Nginx
* Python with Flask
* MongoDB

Detailed instructions on [server setup](./server_setup.html)

## [Data Import](./data_import.html)

Data will come from anywhere. Currently we are focusing on canvasing data from Neighborhoods in NYC affected by Hurricane Sandy. Raw data will come in via `.csv` files. The `.csv` files will be mapped to a document-oriented database.

Each data set will need it's own legend for mapping column headers to the data structure. For instance here's a snippet of code for turning human readable questions into a more structured format:

	'Do you have heat?' : 'have-heat',
	'Do you have plumbing?' : 'have-plumbing',
	'Is the water clean?' : 'have-water-potable',
	'Are there children living here?' : 'have-children'

As common core data sets are created this process can be made more automated.

Detailed instructions on [Data Import](./data_import.html)

## [RESTful API development](./restful_api)

Once the data is *in* the server there needs to be a strategy for getting the data out.

By using Python and Flask we can build custom RESTful API endpoints to serve data. Currently the strategy is to serve `JSON`, but this could be developed to serve `.csv` or `.pdf`.

More details on the [RESTful API development](./restful_api)

# Proof Of Concept

The current proof of concept is based on Canvasing data collected January 19th, 2013 in Staten Island NYC. You can download the non-private data: [anon_SI1.csv](./raw_data/anon_SI1.csv)

This data was then passed through [parse-and-load.py](https://github.com/dhornbein/DataAnywhere/blob/master/occupysandy/db_injection/parse-and-load.py) and injected into a MongoDB.

{% highlight python %}
#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from pymongo import MongoClient
from pandas import read_csv
from math import isnan
import sys
sys.path.append('..')
import config

# a helper class for a legend
#   fill in only the overrides
class LegendOverrides(dict):
	def __missing__(self, key):
		return key
class NormalizeValues(dict):
	def __getitem__(self, key):
		value = dict.__getitem__(self, key)
		if callable(value):
			value = value(key)
		return value
	def __missing__(self, key):
		return key

if __name__ == '__main__':
	# configure the following
	filename = '/home/dtuser/os_deid/anon_SI1.csv'
	date_column_nums = [1]
	legend = LegendOverrides({
		'gid' : 'gid',
		'timestamp' : 'timestamp',
		'Date' : 'date',
		'Zone' : 'project-zone',
		'Preferred Language (if translator needed)?' : 'contact-lang',
		'City' : 'city',
		'State' : 'state',
		'Zipcode' : 'zip',
		'# of Occupants' : 'occupant-count',
		'Are you living here now?' : 'resident',
		'Rent or Own?' : 'rent-or-own-1',
		'Rent or Own? 2' : 'rent-or-own-2',
		'If not here, where are you staying?' : 'residence-other',
		'Do you need a safe place to sleep?' : 'need-shelter',
		'Does anyone in your household need food?' : 'need-food',
		'Do you have electricity?' : 'have-electricity',
		'Do you have water?' : 'have-water',
		'Do you have heat?' : 'have-heat',
		'Do you have plumbing?' : 'have-plumbing',
		'Is the water clean?' : 'have-water-potable',
		'Are there children living here?' : 'have-children',
		'Are there senior citizens living here?' : 'have-seniors',
		'Are there disabled people living here?' : 'have-disabled',
		'What is your country of origin?' : 'contact-origin',
		'Did you stay at home during Sandy?' : 'resident-during-sandy',
		'Was your house damaged?' : 'house-has-damage',
		'Do you have a mold problem?' : 'house-has-mold',
		'Do you need help with repairs?' : 'need-help-repair',
		'Does anyone in your household need medical attention?' : 'need-medical',
		'Is anyone at home feeling stressed out?' : 'have-stress',
		'Does anyone need to speak with a lawyer?' : 'need-lawyer',
		'Does anyone need to speak with a lawyer? 2' : 'need-lawyer-2',
		'Did you receive Disaster Food Stamps?' : 'have-food-stamps',
		'Do you need help with unemployment benefits?' : 'need-help-unemployment',
		'Have you registered with FEMA?' : 'registered-fema',
		'Did you receive a check from FEMA?' : 'have-payment-fema',
		'Did you receive all the funds you believe you should have received from FEMA?' : 'have-payment-fema-ok',
		'Did you apply for an SBA loan?' : 'applied-sba',
		'If you didn‚Äôt apply for an SBA loan, was it because you were:' : 'note-applied-sba',
		'Name of insurers:' : 'contact-insurer',
		'Did you file an insurance claim?' : 'filed-insurance-claim',
		'Do you have flood insurance?' : 'have-insurance-flood',
		'Have you received your flood insurance payment?' : 'have-insurance-flood-payment',
		'Did the payment cover all repairs?' : 'have-insurance-flood-payment-ok',
		'If insurance payment was insufficient, or claim denied, did you file an appeal?' : 'have-insurance-flood-payment-appeal',
		'If insurance payment was insufficient, or claim denied, did you file an appeal? 2' : 'have-insurance-flood-payment-appeal-2',
		'Would you accept help from an attorney with filing an insurance appeal?' : 'need-insurance-flood-payment-lawyer',
		'Are you having mortgage problems?' : 'have-mortage-problem',
		'Do you need legal help with lender problems?' : 'need-loan-lawyer',
		'Did you receive FEMA rental assistance to help you with leasing a temporary or permanent apartment?' : 'have-payment-fema-rental',
		'Did you rent out any part of your home pre-Sandy?' : 'house-rental-by-owner',
		'Would you be interested in attending a community meeting?' : 'interested-attend-meeting',
		'What is your greatest need?' : 'note-need-greatest',
		'Response' : '????',
		'Stickers on house?' : 'have-house-sticker',
		'If free non-perishable food was available ongoing in your community, would this be helpful?' : 'need-food-nonperishable',
		'Any specific details for medical attention?' : 'note-need-medical',
		'Were you told not to register FEMA or not allowed to register with FEMA?' : 'register-fema-denied',
		'Would you accept help from an attorney for your FEMA appeal?' : 'need-fema-appeal-lawyer',
		'Was any portion of this house used as a rental unit pre-Sandy?' : 'house-rental',
		'If not, do you need FEMA rental assistance to help you with leasing a temporary or permanent apartment?' : 'need-rental-assistance-fema',
		'CONTACT INFO NOTES' : 'note-contact',
		'BASIC INFO NOTES' : 'note-info',
		'FEMA/SBA NOTE' : 'note-fema-sba',
		'INSURANCE NOTES' : 'note-insurance',
		'HOUSING NOTES' : 'note-housing',
		'OTHER NOTES' : 'note-other',
		'What subject(s) do these additional notes apply to?' : 'note-other-subjects',
		'Zone Number' : 'project-zone-number'
	})
	normalizations = NormalizeValues({
		u'YES': lambda value: True,
		u'NO': False, })
	# read the data using pandas.read_csv
	data = read_csv(filename, parse_dates=date_column_nums).transpose()

	# normalise data
	cleaned_data = []
	for record in data.to_dict().itervalues():
		# clean n/a and nan fields out
		# there's probably a better way to do this in pandas
		cleaned_record = {legend[k]:normalizations[v] for k,v in record.iteritems() if v and not (isinstance(v,float) and isnan(v)) and v != 'n/a'}

		cleaned_data.append(cleaned_record)
		#print cleaned_data

	# connect to mongo and insert
	with MongoClient(host=config.host, port=config.port) as client:
		for record in cleaned_data:
			# insert into your database.collection (configure this)
			config.sandy_collection.insert(record)
{% endhighlight %}

We then use Python and Flask to create API end points using [flask_os_data.py](https://github.com/dhornbein/DataAnywhere/blob/master/occupysandy/ReST/flask_os_data.py)

{% highlight python %}
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

@app.route('/2/',methods=['GET'])
@app.route('/2/<string:fields_values>',methods=['GET'])
def query_structure(fields_values = False):
    if fields_values:
        request_dict = parse_fields_values(fields_values)

        #search data for request dictionary
        results = [x for x in config.sandy_collection.find(request_dict).limit(50000)]
    else:
        results = [x for x in config.sandy_collection.limit(50000)]
    
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
                    'state':r.pop('state',None),
                    'zip':r.pop('zip',None)
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
                    },
                'notes':{
                    'note-contact':r.pop('note-contact',None),
                    'note-info':r.pop('note-info',None),
                    'note-fema-sba':r.pop('note-fema-sba',None),
                    'note-insurance':r.pop('note-insurance',None),
                    'note-housing':r.pop('note-housing',None),
                    'note-other':r.pop('note-other',None)
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

    return jsonify(count=str(len(results)),items=outbound)
    #return render_template('nonexistent.html', items=items)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    app.run(config.query_f_server,config.query_f_port)
{% endhighlight %}

(Drew:) Don't mind that second function, I'm just playing around with format, but this should be done on the database side.

Now we can ask our server for some data, like so:

![URL bar showing link](http://i.imgur.com/ZYxBkVk.png)

Which returns the following (this is just one item):

{% highlight javascript %}
{
      "timestamp": "2013-02-16T14:49:07Z", 
      "date": null, 
      "home": {
        "occupant-count": null, 
        "have-disabled": null, 
        "residence-other": "Family/Friend", 
        "have-seniors": false, 
        "have-children": true, 
        "resident": false, 
        "rent-or-own-1": null, 
        "rent-or-own-2": "OWN", 
        "damage": {
          "need-help-repair": true, 
          "house-has-mold": true, 
          "house-has-damage": true
        }
      }, 
      "id": "51328f9b2ceea80e0930fd2d", 
      "sandy": {
        "resident-during-sandy": false
      }, 
      "notes": {
        "note-insurance": "got $11,000 from insurance. and was told by FEMA that it was adequate?? electricity repair cost was $5,500.  needs help with dealing with mortgage company.", 
        "note-contact": null, 
        "note-housing": null, 
        "note-other": "can't move back in without floors.  has plywood to replace subfloor.  send grants list.", 
        "note-info": "currently on medical leave from Board of Education, needs food deliveries. rapid repairs screwed up heating so it's getting fixed on 2/18/13.  rapid repairs flooded attic.  evacuated when water reached knees.  has spots of mold on subfloors.", 
        "note-fema-sba": "might be eligible for unemployment because of stroke.  denied FEMA because didn't have inspection.  denied by SBA."
      }, 
      "contact": {
        "contact-origin": null, 
        "contact-lang": null, 
        "phone": null, 
        "first-name": null, 
        "email": null, 
        "last-name": null
      }, 
      "other": {
        "need-medical": true, 
        "house-rental": false, 
        "need-fema-appeal-lawyer": true, 
        "note-need-greatest": "Repairs", 
        "need-food": false, 
        "need-lawyer-2": true, 
        "need-rental-assistance-fema": true, 
        "????": "Completed", 
        "register-fema-denied": false, 
        "need-loan-lawyer": true, 
        "have-insurance-flood": false, 
        "need-shelter": false, 
        "have-heat": false, 
        "have-seriors": false, 
        "have-mortage-problem": true, 
        "have-electricity": true, 
        "filed-insurance-claim": "Yes", 
        "have-payment-fema": true, 
        "have-food-stamps": false, 
        "have-water": true, 
        "have-water-potable": true, 
        "have-insurance-flood-payment-ok": false, 
        "need-help-unemployment": true, 
        "applied-sba": true, 
        "have-house-sticker": "None", 
        "have-stress": true, 
        "have-payment-fema-rental": "received original $2900 but put into repairs", 
        "note-need-medical": "both asthmatic, difficult breathing because of mold.  husband goes to house to feed animals.  she needs medical attention bus is taking care of health.", 
        "have-plumbing": true, 
        "have-insurance-flood-payment-appeal": false, 
        "contact-insurer": "State Farm", 
        "need-food-nonperishable": true, 
        "have-payment-fema-ok": false, 
        "registered-fema": true, 
        "need-insurance-flood-payment-lawyer": true, 
        "interested-attend-meeting": true
      }, 
      "location": {
        "city": "Staten Island", 
        "state": "NY", 
        "street": null, 
        "zip": "10305"
      }, 
      "project-zone": null, 
      "gid": "SI1_1108"
    }
{% endhighlight %}

Now this is where the magic happens, we can feed this into a third party app to parse the data, here's a [really quick example](http://dev.dhornbein.com/t/dataanywhere/)

Checkout the [GitHub Repo](https://github.com/dhornbein/DataAnywhere)

Or email Drew: hello /at/ dhornbein.com

[1]: http://occupydatanyc.org/2013/03/03/data-anywhere-project-hackathon-day-two/
[2]: http://occupydatanyc.org/2013/02/12/open-data-project/
[3]: http://occupysandy.org
[4]: http://blog.dhornbein.com/2013/03/07/data-anywhere-distributed-data-storage-and-sharing-solution/
