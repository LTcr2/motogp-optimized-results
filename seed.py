
"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import Competitor
from model import Team
from model import Result
from model import Venue 

from model import connect_to_db, db
from server import app
from datetime import datetime



def load_competitors():
	"""Load competitors from r.rider into database. """

	print("Competitors")

	for i, row in enumerate(open("seed_data/r.rider")):
		row = row.rstrip()
		generated, schema, competitor, teams, info = row.split(":")

		#creating an instance?
		rider = Competitor(competitor_id=competitor_id,
						   name=name,
						   country_code=country_code,
						   vehicle_number=vehicle_number,
						   result=result,
						   team=team)

		#adding to the session or it won't be stored
		db.session.add(rider)

		#not sure what this line is doing
		#ratings said "provide some sense of progress"
		if i % 100 == 0:
			print(i)

	#commit our work once we're done.... with whatever is above lol
	db.session.commit()

