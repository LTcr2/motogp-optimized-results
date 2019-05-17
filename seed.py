
"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import Competitor, Team, Result, Venue
from model import connect_to_db, db
# from server import app
from datetime import datetime
import json
from server import app



riders_json = "seed_data/riders.json"

"""Using seed.py from ratings lab as an example"""


def load_competitors(riders_json):
	"""refactoring 3 functions into one.
	1. convert json file of rider information and final standings into python dict
	2. parse each piece of their information and create a Competitor object with the extracted information
	3. add riders into the database
	"""

	json_open = open(riders_json).read()
	py_dict = json.loads(json_open)
	rider_list =  []
	for rider in py_dict:
		#print(rider)
		competitor_id = rider['id']
		name = rider['name']
		gender = rider['gender']
		country_code = rider['country_code']
		result = rider['result']
		bike_number = result['bike_number']
		competitor = Competitor(competitor_id=competitor_id, name=name, country_code=country_code, vehicle_number=bike_number)
		print(competitor)

		db.session.add(competitor)

	db.session.commit()




	








if __name__ == "__main__":
	connect_to_db(app)
	db.create_all()

	riders_json = "seed_data/riders.json"
	load_competitors(riders_json)




