import pymongo

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Weather related
data_dir = '../raw_data'
connection = pymongo.Connection()
weather_db = pymongo.database.Database(connection,'weather')
weather_collection = weather_db['air_temp_precip']
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Flask config
query_f_server='127.0.0.1'
query_f_port=5000

