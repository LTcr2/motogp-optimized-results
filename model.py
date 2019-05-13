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

class Competitor(db.Model):
	"""Competitor"""

	__tablename__ = "competitors"


	#one competitor can only have one team, team can have multiple riders

	#referential integrity prevents competitor_id in team table but not in competitor table

	#cannot delete from competitor table if competitor has team

	competitor_id = db.Column(db.Interger, db.ForeignKey('team.team_id'), nullable=False)
	

	name = db.Column(db.String(50), nullable=False)
	country_code = db.Column(db.String(3), nullable=False)
	nationality = db.Column(db.String(3), nullable=False)
	official_website = db.Column(db.String(100), nullable=True)
	debut = db.Column(db.Date, nullable=False)
	gender = db.Column(db.String(10), nullable=False)
	vehicle_number = db.Column(db.Interger, nullable=False)

	"""
	- connect to results and Team
	- establishes SQLAlchemy relationship between tables
	- can use attributes results and team, not a field in the table but a "magic attribute"
	- returns objects or list of objects
	"""

	result = db.relationship('Results')
	team = db.relationship('Team'), db.ForeignKey('team.id')

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

		return "<Competitor id={} name={} nationality={} debut={} gender={} team={}".format(
			self.competitor_id, self.name, self.country_code, self.debut, self.gender, self.team.name)



class Team(db.Model):
	"""Team information"""

	__tablename__ = "teams"

	team_id = db.Column(db.Interger, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	foundation_year = db.Column(db.Date, nullable=False)
	location = db.Column(db.String(70), nullable=False)
	official_website = db.Column(db.String(100), nullable=True)
	vehicle_chassis = db.Column(db.String(50), nullable=False)
	country_code = db.Column(db.String(3), nullable=False)

	competitor = db.relationship('Competitor')



	def __repr__(self):
		
		return "<id={} name={} foundation_year={} location={} vehicle_chassis={} country_code={}".format(
			self.team_id, self.name, self.foundation_year, self.location, self.vehicle_chassis, self.country_code)




class Results(db.Model):
	"""Results is the middle table that connects riders with results table and venue"""

	__tablename__ = "results"

	fastest_lap_time = db.Column(db.DateTime, nullable=False)
	gap = db.Column(db.DateTime, nullable=False, default=00:00:00:000)
	grid = db.Column(db.Integer, nullable=False) #how to add P in front of position integer on grid
	laps = db.Column(db.Integer, nullable=False)
	podiums = db.Column(db.Integer, nullable=False)
	points = db.Column(db.Integer, nullable=False)
	position = db.Column(db.Integer, nullable=False)
	vehicle_number = db.Column(db.Integer, nullable=False)
	status = db.Column(db.Boolen, nullable=False)
	victories = db.Column(db.Integer, nullable=False)
	victory_pole_fastest_lap = db.Column(db.Integer, nullable=False)

	#create a variable that is based on the value that exists in the venue
	venue = db.relationship('Venue.venue_id')
	competitor = db.relationship('Competitor', backref='result')

	def __repr__(self):
		"""Define and display all the values of the result."""

		return"<Result fastest_lap_time={} gap={} grid={} laps={} podiums={} points={} position={} vehicle_chassis={} status={} victories={} victory_pole_fastest_lap={}".format(
			self.fastest_lap_time, self.gap, self.grid, self.laps, self.podiums, self.points, self.position, self.vehicle_chassis, self.status, self.victories, self.victory_pole_fastest_lap)




class Venue(db.Model):
	"""Track information"""

	__tablename__ = "venues"

	venue_id = db.Column(db.Integer, primarykey=True, nullable=False)
	city = db.Column(db.String(50), nullable=False)
	name = db.Column(db.String(50), nullable=True)
	country = db.Column(db.String(50), nullable=False)
	country_code = db.Column(db.String(3), nullable=False)
	curves_left = db.Column(db.Integer, nullable=False)
	curves_right = db.Column(db.Integer, nullable=False)
	turns = db.Column(db.Integer(curves_left + curves_right))


	def __repr__(self):
		"""Define and display Venue class information"""

		return "<Venue id={} city={} country={} country code={} lefts={} rights={} turns={}".format(
			self.venue_id, self.city, self.country, self.country_code, self.curves_left, self.curves_right, self.turns)

















####################################################
# Helper functions ??? (I'm not sure what this means, took it from the SQLAlchemy lecture demo)

def connect_to_db(app):
	"""Connect the database to our Flask App."""

	#Configure to use our Postgres databse
	app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql:///results' #double check this 
	app.config['SQLALCHEMY_ECHO'] = True
	db.app = app
	db.init_app(app)

if __name__ == "__main__":
	# As a convenience, if we run this module interactively, it will leave you in a state of being able to work with the database directly.

	# So that we can use Flask-SQLAlchemy, we'll make a Flask app
	from flask import Flask

	app = Flask(__name__)

	connect_to_db(app)
	print("Connected to theeee DB.")

	db.create_all()
	example_data()





