"""Using SQLAlchemy, joins & relationships to handle database

Something I can't say I really understand right now
"""

from flask_sqlalchemy import SQLAlchemy

"""
This is our connection to the databse; we're getting this through the Flask-SQLAlchemy helper library.

We also can find `session` object, where we can do our interactions like committing.
"""

db = SQLAlchemy()

####################################################
# Model definitions

# WE DON'T NEED A SEASON because our data is only 2018

class Competitor(db.Model):
	"""Competitor"""

	__tablename__ = "competitors"

	competitor_id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(50),nullable=False)
	country_code = db.Column(db.String(3), nullable=False)
	# nationality = db.Column(db.String(3), nullable=False)
	# official_website = db.Column(db.String(100), nullable=True)
	# debut = db.Column(db.Date, nullable=False)
	# gender = db.Column(db.String(10), nullable=False)
	vehicle_number = db.Column(db.Integer, nullable=False)

	"""
	- connect to results and Team
	- establishes SQLAlchemy relationship between tables
	- can use attributes results and team, not a field in the table but a "magic attribute"
	- returns objects or list of objects
	"""

	# result = db.relationship('Result'), db.ForeignKey('competitor_id')
	team = db.Column(db.String, nullable=True)

	"""
	alternative relationship syntax: backref
	- using "backref" in the relationship definition on Book allows you to create both relationships in a single statement
	
	class Competitor(db.Model):

		team = db.relationship('Team', backref='competitor')
	class Team(db.Model):
		...

	"""


	def __repr__(self):
		""" Returns representation of class information"""

		return "<Competitor id={} name={} nationality={} vehicle_number={} team={}".format(
			self.competitor_id, self.name, self.country_code, self.vehicle_number, self.team)



class Team(db.Model):
	"""Team information"""

	__tablename__ = "teams"

	team_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	country_code = db.Column(db.String(3), nullable=False)

	position = db.Column(db.Integer, nullable=False)
	podiums = db.Column(db.Integer, nullable=True)
	points = db.Column(db.Integer, nullable=True)
	victories = db.Column(db.Integer, nullable=True)
	# vehicle_chassis = db.Column(db.String(50), nullable=False)
	# foundation_year = db.Column(db.Date, nullable=False)
	# competitor = db.relationship('Competitor')

	#### probably don't need these ####
	# location = db.Column(db.String(70), nullable=False)
	# official_website = db.Column(db.String(100), nullable=True)
	



	def __repr__(self):
		
		return "<Team id={} name={} country_code={} victories={} position= {} podiums={}".format(
			self.team_id, self.name, self.country_code, self.victories, self.position, self.podiums, self.points)




class Result(db.Model):
	"""Results is the middle table that connects riders with results table and venue"""

	__tablename__ = "results"

	#i might need this id to refer to a specific result..
	rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	fastest_lap_time = db.Column(db.String, nullable=False)
	gap = db.Column(db.String, nullable=False)
	position = db.Column(db.Integer, nullable=False)

	# grid = db.Column(db.Integer, nullable=False) #how to add P in front of position integer on grid
	# laps = db.Column(db.Integer, nullable=True)
	# podiums = db.Column(db.Integer, nullable=True)
	# points = db.Column(db.Integer, nullable=True)
	# pole_positions = db.Column(db. Integer, nullable=True)
	# status = db.Column(db.String, nullable=False)
	# victories = db.Column(db.Integer, nullable=False)
	# victory_pole_fastest_lap = db.Column(db.Integer, nullable=False)

	#create a variable that is based on the value that exists in the venue

	venue_id = db.Column(db.Integer,
						 db.ForeignKey('venues.venue_id'))
	competitor_id = db.Column(db.Integer,
							  db.ForeignKey('competitors.competitor_id'))
	venue = db.relationship("Venue",
							backref=db.backref("results",
												order_by=position))
	competitor = db.relationship("Competitor", 
									backref=db.backref("results",
														order_by=position))


	def __repr__(self):
		"""Define and display all the values of the result."""

		return"<Result id={} fastest_lap_time={} gap={} grid={} laps={} podiums={} points={} position={} vehicle_chassis={} status={} victories={} victory_pole_fastest_lap={}".format(
			self.rating_id, self.fastest_lap_time, self.gap, self.grid, self.laps, self.podiums, self.points, self.position, self.vehicle_chassis, self.status, self.victories, self.victory_pole_fastest_lap)




class Venue(db.Model):
	"""Track information"""

	__tablename__ = "venues"

	venue_id = db.Column(db.Integer, primary_key=True, nullable=False)
	city = db.Column(db.String(50), nullable=False)
	name = db.Column(db.String(100), nullable=True)
	# country = db.Column(db.String(50), nullable=False)
	country_code = db.Column(db.String(3), nullable=False)
	description = db.Column(db.String(150), nullable=False)
	status = db.Column(db.String(20), nullable=False)
	# lefts = db.Column(db.Integer, nullable=False)
	# rights = db.Column(db.Integer, nullable=False)
	length = db.Column(db.Float, nullable=False)
	# debut = db.Column(db.Integer, nullable=False)
	turns = db.Column(db.Integer, nullable=False)
	latitude = db.Column(db.Float, nullable=False)
	longitude = db.Column(db.Float, nullable=False)


	def __repr__(self):
		"""Define and display Venue class information"""

		return f"<Venue id={self.venue_id} city={self.city} name={self.city} country={self.country_code} description={self.description} status={self.status} length={self.length} turns={self.turns} latitude={self.latitude} longitude={self.longitude}> "











####################################################
# Helper functions ??? (I'm not sure what this means, took it from the SQLAlchemy lecture demo)

def connect_to_db(app):
	"""Connect the database to our Flask App."""

	#Configure to use our Postgres databse
	app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql:///results' #double check this 
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.app = app
	db.init_app(app)

if __name__ == "__main__":
	# As a convenience, if we run this module interactively, it will leave you in a state of being able to work with the database directly.

	# So that we can use Flask-SQLAlchemy, we'll make a Flask app
	from flask import Flask
	# from server import app

	app = Flask(__name__)

	connect_to_db(app)
	print("Connected to theeee DB.")

	db.create_all()





