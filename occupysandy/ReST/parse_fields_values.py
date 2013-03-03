"""
Parsing Flask args to pass to database.
"""

__authors__ = ['Drew Hornbein: foo@bar.com', 'Elizabeth Wiethoff: 718-877-6198']

__all__ = ['parse_fields_values']

import os_data_conf

def parse_fields_values(fields_values):
    """Return a dict to pass to the database.
    Dict contains proper default values for some boolean data fields.
    """

    output = {}

    fv_pairs = fields_values.split('&')
    for fv_pair in fv_pairs:

        # sometimes value will be empty string
        if '=' in fv_pair: field,value = fv_pair.split('=', 1)
        else: field, value = fv_pair, ''

        if field not in os_data_conf.instructions:
            output[field] = value
            continue
        
        instruction = os_data_conf.instructions[field]

        try:
            output[field] = instruction(value)
            continue

        except os_data_conf.IgnoreField:
            output[field] = value

    return output

##########

if __name__ == '__main__':
    string = 'have-heat=0&have-water=Y&occupant-count=3'
    print string, parse_fields_values(string)

    string = 'have-heat=false&FEMA=Pending&occupant-count=foo'
    print string, parse_fields_values(string)

    string = 'have-heat&need-lawyer'
    print string, parse_fields_values(string)
