# build_config.py
#
# Input: .csv (or more...)
## should accept a .csv (etc.) files from command line argument like so: `build_config.py your_data.csv ...`
# Output: Column headers as associative .YAML array 
## with blank keys matching the outline in `config.yaml.sample`
## output to name: config.[csv_file_name].yaml
## confirm if overwrite
