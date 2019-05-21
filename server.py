from jinja2 import StrictUndefined
from flask import Flask, jsonify, request, render_template, redirect, session, flash

from sqlalchemy import func
from model import Competitor, Team, Result, Venue, connect_to_db, db

import requests
import json
# from flask_debugtoolbar import DebugToolbarExtension

#using api lab "balloonicorn's party" from hackbright as example

#MY UNIQUE QUERY PARAMETERS
app = Flask(__name__)

app.secret_key = "NOTSUREYETBUTOKAY"
app.jinja_env.undefined = StrictUndefined
sportradar_url = "http://api.sportradar.us/motogp/trial/v2/en/"
access_level = 'trial'
version = 'v2'
language_code = 'en'
return_format = 'json'
your_api_key = 't2pxakdxpkskhr3ajc3rgb72'
url = "http://api.sportradar.us/motogp/trial/v2/en/competitors/sr:competitor:21999/profile.json?api_key=t2pxakdxpkskhr3ajc3rgb72"
headers = {'Authorization': 'Bearer' + your_api_key}
response = requests.get(url)
data = response.json()
print(data['schema'])



"""
Endpoint format:

https://api.sportradar.us/motogp/{access_level}/{version}/{language_code}/competitors/{competitor_id}/profile.{return_format}?api_key={your_api_key}
"""



@app.route("/")
def homepage():
	"""Show homepage"""

	return render_template("/homepage.html")


### First try at getting just 'Marc Marquez' and storing it as a variable ###
@app.route("/competitors", methods=['GET'])
def competitor_list():
	"""get info from API endpoints, 
	convert from json to python dictionary,
	write to database.

	motogp/trial/v2/en/competitors/:competitor_id/profile:format
	"""
	competitors = Competitor.query.all()
	return render_template('/competitors_list.html', competitors=competitors)


@app.route("/competitors/<int:competitor_id>")
def competitor_detail(competitor_id):
	"""Show info about specific rider"""

	competitor = Competitor.query.get(competitor_id)
	return render_template('/competitor.html', competitor=competitor)


@app.route("/teams")
def teams_list():
	"""Show list of teams"""

	teams = Team.query.order_by('points').all()
	return render_template('teams.html', teams=teams)

@app.route("/teams/<int:team_id", methods=['GET'])
def team_detail():
	"""Show info about a specific team"""

	team = Team.query.get(team_id)
	return render_template('teams.html', team=team)



@app.route("/venues")
def venue_list():
	"""Show list of stages in the 2018 Championship"""

	venues = Venue.query.all()
	return render_template('venues.html')


@app.route("/venues/<int:venue_id", methods=['GET'])
def venue_detail(venue_id):
	"""Show details about a specific venue"""

	venue = Venue.query.get(venue_id)
	return render_template('venues.html', venue=venue)

















if __name__ == "__main__":

	app.debug = True

	connect_to_db(app)

	DebugToolbarExtension(app)

app.run(host="0.0.0.0")



# if __name__ == '__main__':
# 	connect_to_db(app)

# 	manager = APIManager(app, flask_sqlalchemy_db=db)

# 	# Create API endpoints, which will be available at /api/<tablename> by default. Allowed HTTP methods can be specified as well.

# 	manager.create_api(
# 		Competitor,
# 		methods = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])

# 	manager.create_api(
# 		Team,
# 		methods = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])

# 	manager.create_api(
# 		Result,
# 		methods = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])

# 	manager.create_api(
# 		Venue,
# 		methods = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
