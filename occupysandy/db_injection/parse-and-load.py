#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

from pymongo import MongoClient
from pandas import read_csv
from math import isnan
import sys
sys.path.append('..')
import config

# a helper class for a legend
#   fill in only the overrides
class LegendOverrides(dict):
	def __missing__(self, key):
		return key
class NormalizeValues(dict):
	def __getitem__(self, key):
		value = dict.__getitem__(self, key)
		if callable(value):
			value = value(key)
		return value
	def __missing__(self, key):
		return key

if __name__ == '__main__':
	# configure the following
	filename = '/home/dtuser/os_deid/anon_SI1.csv'
	date_column_nums = [1]
	legend = LegendOverrides({
		'gid' : 'gid',
		'timestamp' : 'timestamp',
		'Date' : 'date',
		'Zone' : 'project-zone',
		'Preferred Language (if translator needed)?' : 'contact-lang',
		'City' : 'city',
		'State' : 'state',
		'Zipcode' : 'zip',
		'# of Occupants' : 'occupant-count',
		'Are you living here now?' : 'resident',
		'Rent or Own?' : 'rent-or-own-1',
		'Rent or Own? 2' : 'rent-or-own-2',
		'If not here, where are you staying?' : 'residence-other',
		'Do you need a safe place to sleep?' : 'need-shelter',
		'Does anyone in your household need food?' : 'need-food',
		'Do you have electricity?' : 'have-electricity',
		'Do you have water?' : 'have-water',
		'Do you have heat?' : 'have-heat',
		'Do you have plumbing?' : 'have-plumbing',
		'Is the water clean?' : 'have-water-potable',
		'Are there children living here?' : 'have-children',
		'Are there senior citizens living here?' : 'have-seniors',
		'Are there disabled people living here?' : 'have-seriors',
		'What is your country of origin?' : 'contact-origin',
		'Did you stay at home during Sandy?' : 'resident-during-sandy',
		'Was your house damaged?' : 'house-has-damage',
		'Do you have a mold problem?' : 'house-has-mold',
		'Do you need help with repairs?' : 'need-help-repair',
		'Does anyone in your household need medical attention?' : 'need-medical',
		'Is anyone at home feeling stressed out?' : 'have-stress',
		'Does anyone need to speak with a lawyer?' : 'need-lawyer',
		'Does anyone need to speak with a lawyer? 2' : 'need-lawyer-2',
		'Did you receive Disaster Food Stamps?' : 'have-food-stamps',
		'Do you need help with unemployment benefits?' : 'need-help-unemployment',
		'Have you registered with FEMA?' : 'registered-fema',
		'Did you receive a check from FEMA?' : 'have-payment-fema',
		'Did you receive all the funds you believe you should have received from FEMA?' : 'have-payment-fema-ok',
		'Did you apply for an SBA loan?' : 'applied-sba',
		'If you didn‚Äôt apply for an SBA loan, was it because you were:' : 'note-applied-sba',
		'Name of insurers:' : 'contact-insurer',
		'Did you file an insurance claim?' : 'filed-insurance-claim',
		'Do you have flood insurance?' : 'have-insurance-flood',
		'Have you received your flood insurance payment?' : 'have-insurance-flood-payment',
		'Did the payment cover all repairs?' : 'have-insurance-flood-payment-ok',
		'If insurance payment was insufficient, or claim denied, did you file an appeal?' : 'have-insurance-flood-payment-appeal',
		'If insurance payment was insufficient, or claim denied, did you file an appeal? 2' : 'have-insurance-flood-payment-appeal-2',
		'Would you accept help from an attorney with filing an insurance appeal?' : 'need-insurance-flood-payment-lawyer',
		'Are you having mortgage problems?' : 'have-mortage-problem',
		'Do you need legal help with lender problems?' : 'need-loan-lawyer',
		'Did you receive FEMA rental assistance to help you with leasing a temporary or permanent apartment?' : 'have-payment-fema-rental',
		'Did you rent out any part of your home pre-Sandy?' : 'house-rental-by-owner',
		'Would you be interested in attending a community meeting?' : 'interested-attend-meeting',
		'What is your greatest need?' : 'note-need-greatest',
		'Response' : '????',
		'Stickers on house?' : 'have-house-sticker',
		'If free non-perishable food was available ongoing in your community, would this be helpful?' : 'need-food-nonperishable',
		'Any specific details for medical attention?' : 'note-need-medical',
		'Were you told not to register FEMA or not allowed to register with FEMA?' : 'register-fema-denied',
		'Would you accept help from an attorney for your FEMA appeal?' : 'need-fema-appeal-lawyer',
		'Was any portion of this house used as a rental unit pre-Sandy?' : 'house-rental',
		'If not, do you need FEMA rental assistance to help you with leasing a temporary or permanent apartment?' : 'need-rental-assistance-fema',
		'CONTACT INFO NOTES' : 'note-contact',
		'BASIC INFO NOTES' : 'note-info',
		'FEMA/SBA NOTE' : 'note-fema-sba',
		'INSURANCE NOTES' : 'note-insurance',
		'HOUSING NOTES' : 'note-housing',
		'OTHER NOTES' : 'note-other',
		'What subject(s) do these additional notes apply to?' : 'note-other-subjects',
		'Zone Number' : 'project-zone-number'
	})
	normalizations = NormalizeValues({
		u'YES': lambda value: True,
		u'NO': False, })
	# read the data using pandas.read_csv
	data = read_csv(filename, parse_dates=date_column_nums).transpose()

	# normalise data
	cleaned_data = []
	for record in data.to_dict().itervalues():
		# clean n/a and nan fields out
		# there's probably a better way to do this in pandas
		cleaned_record = {legend[k]:normalizations[v] for k,v in record.iteritems() if v and not (isinstance(v,float) and isnan(v)) and v != 'n/a'}

		cleaned_data.append(cleaned_record)
		#print cleaned_data

	# connect to mongo and insert
	with MongoClient(host=config.host, port=config.port) as client:
		for record in cleaned_data:
			# insert into your database.collection (configure this)
			config.sandy_collection.insert(record)
