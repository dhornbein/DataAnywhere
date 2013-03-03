import functools

class IgnoreField(StandardError): pass

def process_int(string, default):
	try: return int(string)
	except ValueError: return default

process_int_default_0 = functools.partial(process_int, default=0)

def process_bool(string, default):
	if string == '': return default
	string = string.lower()
	if string in {'1', 'y', 'yes', 'true'}: return True
	if string in {'0', 'n', 'no', 'false'}: return False
	return default

process_bool_default_true = functools.partial(process_bool, default=True)
process_bool_default_false = functools.partial(process_bool, default=False)

##########

instructions = {
	'occupant-count': process_int_default_0,
	'need-shelter': process_bool_default_true,
	'need-food': process_bool_default_true,
	'have-electricity': process_bool_default_true,
	'have-plumbing': process_bool_default_true,
	'have-water-potable': process_bool_default_true,
	'have-children': process_bool_default_true,
	'have-seniors': process_bool_default_true,
	'house-has-damage': process_bool_default_true,
	'house-has-mold': process_bool_default_true,
	'need-help-repair': process_bool_default_true,
	'need-medical': process_bool_default_true,
	'have-stress': process_bool_default_true,
	'have-heat': process_bool_default_true,
	'have-water': process_bool_default_true,

}
