
"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from datetime import datetime
from sqlalchemy import func
from model import Competitor, Team, Result, Venue, connect_to_db, db
import json
from server import app


"""Using seed.py from ratings lab as an example"""


def load_competitors(riders_json):
	"""refactoring 3 functions into one.
	1. convert json file of rider information and final standings into python dict
	2. parse each piece of their information and create a Competitor object with the extracted information
	3. add riders into the database
	"""

	json_open = open(riders_json).read()
	py_dict = json.loads(json_open)
	for rider in py_dict:
		#print(rider)
		competitor_id = rider['id']
		name = rider['name']
		gender = rider['gender']
		country_code = rider['country_code']
		result = rider['result']
		bike_number = result['bike_number']
		team = rider['team']
		team_name = team['name']
		competitor = Competitor(competitor_id=competitor_id, 
							name=name, 
							vehicle_number=bike_number, 
							team=team_name,
							country_code=country_code)
		print(competitor)
		# else:
		# 	competitor = Competitor(competitor_id=competitor_id, 
		# 							name=name, 
		# 							vehicle_number=bike_number,
		# 							team=None,
		# 							country_code=country_code)

		db.session.add(competitor)
	db.session.commit()

	# import pdb; pdb.set_trace()


def load_teams(teams_json):
	"""load teams json into data base"""

	py_dict = json.loads(open(teams_json).read())
	for team in py_dict:
		team_id = team['id']
		name = team['name']
		country_code = team['country_code']
		result = team['result']
		position = result['position']
		points_check = result.get('points', 0)
		podiums_check = result.get('podiums', 0)
		victories_check = result.get('victories', 0)


		team = Team(team_id=team_id, 
					name=name,
					country_code=country_code,
					position=position,
					points=points_check,
					podiums=podiums_check,
					victories=victories_check)
		print(team)

		db.session.add(team)
	db.session.commit()

	# import pdb; pdb.set_trace()

def load_venues(venues_json):
	"""load venues & information into database"""

	# import pdb; pdb.set_trace()

	py_dict = json.loads(open(venues_json).read())
	for venue in py_dict:
		venue_id = venue['id']
		city = venue['city']
		name = venue['name']
		country_code = venue['country_code']
		description = venue['description']
		status = venue['status']
		length = venue['length']
		turns = venue['turns']
		venue = Venue(venue_id=venue_id, 
					  city=city, 
					  name=name,
					  country_code=country_code, 
					  description=description, 
					  status=status,
					  length=length,
					  turns=turns,)
		print(venue)

		db.session.add(venue)
	db.session.commit()

	# import pdb; pdb.set_trace()

def load_results(results_json):
	"""load results summary into database"""

	# import pdb; pdb.set_trace()

	py_dict = json.loads(open(results_json).read())
	#in py_dict, there is only one key
	#this is 'stage'
	stage = py_dict['stage']
	#in stage, there are these keys
	#'id', 'description', 'scheduled', 'scheduled_end', 'type', 'parents', 'stages', 'competitors', 'teams'
	#STRINGS = id, description, scheduled, scheduled_end, type
	#VALUES = sr:stage:337639, MotoGP 2018, 2018-03-16T11:55:00+00:00, 2018-11-18T14:00:00+00:00, season
	#LIST = Parents = [{'id': 'sr:stage:8306', 'description': 'MotoGP', 'type': 'sport'}]
	stages_list = stage['stages']
	teams_list = stage['teams']
	competitors_list = stage['competitors']

	#To Do:
	#Make Result Instances




	#result = Result(competitor_id=competitor_id
					 # venue_id=venue_id
					 # etc=etc)
					 #################### WORK ON THIS ###########################
	# print(result)

	# db.session.add(result)
	# db.session.commit()



	return(py_dict)

	# for item in py_dict:
	# 	stage = py_dict['stage']
	# 	venues = stage['stages']
	# 	competitors = stage['competitors']
	# 	teams = stage['teams']



if __name__ == "__main__":
	connect_to_db(app)
	db.create_all()

	riders_json = "seed_data/riders.json"
	teams_json = "seed_data/teams.json"
	venues_json = "seed_data/venues.json"
	results_json = "seed_data/results.json"
	# load_competitors(riders_json)
	# load_teams(teams_json)
	# load_venues(venues_json)
	load_results(results_json)




