
"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import Competitor, Team, Result, Venue

from model import connect_to_db, db
from server import app
from datetime import datetime
import json




"""Using seed.py from ratings lab as an example"""


def convertjson_riders():
	"""trying to convert a some json into a python dictionary"""

	json_open = open("seed_data/riders.json").read()

	converted_info = json.loads(json_open)
	# this works! 
	# now now i need to put this parse this data

	#I need to clean this up into rows so I can freakin read it
	cleaned_up = []

	for item in converted_info:
		cleaned_up.append(item)

	#cleaned_up is now a list
	return cleaned_up

def parse(py_list):
	"""take the now python dictionary, take it apart to commit pieces to the db"""

	#loop through the entire document
	"""using enumerate to loop over some list and have an automatic counter
	example:
		my_list = ['apple', 'banana', 'grapes', 'pear']
		for c, value in enumerate(my_list, 1):
    		print(c, value)

	# Output:
	# 1 apple
	# 2 banana
	# 3 grapes
	# 4 pear
    """
	# for item in py_list:

	# 	return item

		# competitor_id, name, gender, nationality, country_code, team, result = 

	rider_names = []

	for item in py_list:
		rider_names.append(item['name'])

	return rider_names

def load_riders(rider_names):
	"""take a list of rider_names and add to db"""

	print("Riders")

	for name in rider_names:
		competitor = Competitor(name=name)

		# we need to add to the session or it won't ever be stored
		db.session.add(competitor)

		#provide some sense of progress
		if i % 100 == 0:
			print(i)

	#once we're done, we should commit our work
	db.session.commit()




if __name__ == "__main__":
	connect_to_db(app)
	db.create_all()

	load_riders()




