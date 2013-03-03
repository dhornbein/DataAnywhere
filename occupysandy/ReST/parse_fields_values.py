import os_data_conf

def parse_fields_values(fields_values):

    output = {}

    fv_pairs = fields_values.split('&')
    for fv_pair in fv_pairs:
        # sometimes value will be empty string
        field,value = fv_pair.split('=',1)

        if field not in os_data_conf.instructions:
            continue
        
        instruction = os_data_conf.instructions[field]
        if isinstance(instruction, dict):
            try:
                output[field] = instruction[value]
            except KeyError:
                continue

        elif callable(instruction):
            try:
                output[field] = instruction(value)
            except os_data_conf.IgnoreField:
                continue

    return output

##########

if __name__ == '__main__':
    string = 'has_heat=0&has_water=Y&number_of_occupants=3'
    print string, parse_fields_values(string)

    string = 'has_heat=false&FEMA=Pending&number_of_occupants=foo'
    print string, parse_fields_values(string)
