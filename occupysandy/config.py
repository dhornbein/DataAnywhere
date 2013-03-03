import pymongo

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Weather related
host='127.0.0.1'
port=27017
data_dir = '../raw_data'
connection = pymongo.Connection()
weather_db = pymongo.database.Database(connection,'weather')
sandy_db = pymongo.database.Database(connection,'sandy')
weather_collection = weather_db['air_temp_precip']
sandy_collection = sandy_db['surveys']
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Flask config
query_f_server='127.0.0.1'
query_f_port=5000

