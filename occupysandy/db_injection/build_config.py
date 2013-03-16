# build_config.py
#
# Input: .csv (or more...)
## should accept a .csv (etc.) files from command line argument like so: `build_config.py your_data.csv ...`
# Output: Column headers as associative .YAML array 
## with blank keys matching the outline in `config.yaml.sample`
## output to name: config.[csv_file_name].yaml
## confirm if overwrite

# !!! this code is writen by an amature, please make it better, smarter, faster. -Drew

import csv
import sys

'''
TODO: Import file from command line argument
'''
csv_file_name = 'test.csv'
raw_csv = './raw_data/' + csv_file_name
f = open(raw_csv, 'rt')

'''
Read the first line of the csv
TODO: what if the csv doesn't have column headers? What if column headers aren't on the first line?!
'''
try:
	data = csv.reader(f)
	header = data.next()
finally:
	f.close()

'''
Build the YAML config file
It would be cool to test a few values from each column and attempt to guess
the data type, normalize function needed, if private is True, and what category
the value belong to....
'''
template = """ 
 readable:
 key:
 normalize:
 private:
 default:
 n_a:
 category:
"""

out = '# automagically compiled with `build_config.py` from ' + csv_file_name
out += "\n---\n" # denotes the start of a YAML file

'''
TODO: Have to make sure value is escaped so it doesn't screw with our sweet little YAML file
'''

for item in header:

	out += '"' + item + '":' + template + "\n"

out += "..." # denotes the end of a YAML file

'''
Write the YAML file
TODO: handle existing versions of config file to prevent overwrite
'''
f = open('./config.' + csv_file_name[:csv_file_name.find('.csv')] + '.yaml','w')

try:
	f.write(out)
finally:
	f.close()