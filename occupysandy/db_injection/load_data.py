# load_data.py
#
# This script takes a .csv file and matches it to a config file
# Example:
## load my_data.csv
## optionaly load config file
## If config file isn't specified the script
## should look for config.my_data.yaml (config.[csv name].yaml)

'''
The following is a novice's sad attempt at outlining the code
be bold and make it better <3 - Drew
'''

# pull in normalize functions
import normalize

# load data file
raw_data = None

# parse raw data into dict
data = raw_data

# if user specifies a config file use that
# else load
if conf:
	conf = None
else
	conf = 'config.' + raw_data[:raw_data.find('.csv')] + '.yaml'

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

