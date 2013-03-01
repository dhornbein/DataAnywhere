import sys
import os
import codecs
import re
import pymongo
sys.path.append('..')
import config

class WeatherData(object):
    def __init__(self):
        self.data_dir = config.data_dir
        self.temp_pattern = 'air_temp\.(\d{4})'
        self.precip_pattern = 'precip\.(\d{4})'

        self.weather_collection = config.weather_collection

    def list_files(self):
        self.temp_files = [f for f in os.listdir(self.data_dir) if f.find(self.temp_pattern.split('\\')[0]) >= 0]
        self.precip_files = [f for f in os.listdir(self.data_dir) if f.find(self.precip_pattern.split('\\')[0]) >= 0]

    def inject_temp(self):
        for f in self.temp_files:

            year = int( re.match(self.temp_pattern,f).group(1) )
            print "Year: %d" % year
            sys.stdout.flush()

            with codecs.open(self.data_dir + '/' + f,'r','utf-8') as tfile: # In case of multilingual text.
                for r in tfile.readlines():
                    r_split = r.split()
                    longitude = r_split[0]
                    latitude = r_split[1]
                    temps_jan_dec = r_split[2:]
                    '''
                    Do Farenheit conversion, round to nearest tenths.
                    '''
                    self.weather_collection.insert(
                        {
                            'year':year,
                            'location':[float(longitude),float(latitude)],
                            'temps_c':[round(float(t),1) for t in temps_jan_dec],
                            'temps_f': [round( ((float(t) * 9) / 5) + 32, 1 ) for t in temps_jan_dec]
                        },
                        safe=True)

        self.weather_collection.create_index([("year", pymongo.ASCENDING)])
        self.weather_collection.create_index([("location", pymongo.GEO2D)])

    def update_precip(self):
        for f in self.precip_files:

            year = int( re.match(self.precip_pattern,f).group(1) )
            print "Year: %d" % year
            sys.stdout.flush()

            with codecs.open(self.data_dir + '/' + f,'r','utf-8') as tfile: # In case of multilingual text.
                for r in tfile.readlines():
                    r_split = r.split()
                    longitude = r_split[0]
                    latitude = r_split[1]
                    precips_jan_dec = r_split[2:]
                    '''
                    Precipitation is in mm.
                    '''
                    self.weather_collection.update(
                        {
                            'year':year,
                            'location':[float(longitude),float(latitude)]
                        },
                        {
                            '$set': {
                                'precips_mm':[round(float(p),1) for p in precips_jan_dec]
                                }
                        },
                        upsert=False,safe=True)

        self.weather_collection.create_index([("year", pymongo.ASCENDING)])
        self.weather_collection.create_index([("location", pymongo.GEO2D)])

    def just_index(self):
        print "indexing..."
        self.weather_collection.ensure_index([("year", pymongo.ASCENDING)])
        self.weather_collection.ensure_index([("location", pymongo.GEO2D)])
        print "done"

if __name__ == "__main__":
   w = WeatherData()
   #w.list_files()
   #w.inject_temp()
   #w.update_precip()
   w.just_index()
