# load_data.py
#
# This script takes a .csv file and matches it to a config file
# Example:
## load my_data.csv
## optionaly load config file
## If config file isn't specified the script
## should look for config.my_data.yaml (config.[csv name].yaml)
# Then it iterates over the .csv data and cleans it up
# conf files contain attributes (see example config.samle.yaml) that are applied to values

'''
The following is a novice's sad attempt at outlining the code
be bold and make it better <3 - Drew
'''
from pymongo import MongoClient
from pandas import read_csv
from pprint import pprint
import os
import sys
sys.path.append('..')
import config
import yaml

# pull in normalize functions
import normalize

# load data file from argument
if len(sys.argv) > 1:
	raw_data = sys.argv[1]
else:
	exit()

# get file name
data_file_name = os.path.splitext(os.path.basename(raw_data))[0]

# load conf_file file from argument or build it from data file name
if len(sys.argv) > 2:
	conf_file = sys.argv[2]
else:
	conf_file = 'config.' + data_file_name + '.yaml'

# parse raw data into dict
data = read_csv(raw_data).transpose()

# load binary
conf = yaml.load(open(conf_file,'rt'))

i = 1
cleaned_data = []
for record in data.to_dict().itervalues():

	r = {'misc':{},'private':{}}
	for k,v in record.iteritems():
		cat = 'misc'
		if k in conf:
			cat = 'question'

			if 'category' in conf[k]:
				cat = conf[k]['category']
				if 'private' in conf[k]:
					if conf[k]['private']: cat = 'private'

				if cat not in r:
					r[cat] = {}
			
			v = normalize.parseNotApplicable(v,'n_a' in conf[k])

			if 'normalize' in conf[k]:
				v = normalize.funcdict[conf[k]['normalize']](v)
			
			k = conf[k]['key']

		r[cat][k] = v

	cleaned_data.append(r)

'''
parseConf()
takes one argument, a yaml config file and returns a dict
* might not need a function
'''
def parseConf(yaml):
	None

'''
Here's the fun part! we unpack the raw_data and 
compare it to the config file
'''
# connect to mongo and insert
with MongoClient(host=config.host, port=config.port) as client:
	for record in cleaned_data:
		# insert into your database.collection (configure this)
		config.sandy_collection.insert(record)
