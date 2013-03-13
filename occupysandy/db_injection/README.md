# Database Injection Section
====
This is where we take our dirty, malformed, error ridden raw data and turn it into a MongoDB data set we can be proud of.

Included in this folder:
* build_config.py
* config.sample.yaml
* normalize.py
* load.py

## build_config.py

This happy little script takes a .csv file, strips the column header values, and builds a base config.yaml file ready to be parsed!

## config.sample.yaml

This file outlines how to structure the config file for the data set. 
The configure file maps the raw data's column name to a tidy name for inside the database,
it also defines the normalize function to run the value through as well as some meta data like
category, private, and n_a

Each column header exists in this config like so:

```yaml
"column header name as it appears in the data set":
 readable: "a human readable version of the text"
 key: "item-slug"
 normalize: functionName
 private: bool
 default: "the default return value if a query string is blank"
 n_a: bool (accept n/a?)
 category: string or [list,of,strings]
 ```

 ## Normalize.py

 A group of functions that are to be run on data values. For instance `parseBool` will take an input string and map it to `True` or `False`
 if the string contains something that can be interperated as such. For instance a value of "yes", "y", or "true" will return `True`

 ## load.py

 This script loads the data file and config file then parses all the data into the MongoDB