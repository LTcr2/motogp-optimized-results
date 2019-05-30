"""MotoGP Results."""

from jinja2 import StrictUndefined
from flask import Flask, jsonify, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import Competitor, Team, Result, Venue, connect_to_db, db

import requests
import json

from sqlalchemy import func

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
# response = requests.get(url)
# data = response.json()
# print(data['schema'])



"""
Endpoint format:

https://api.sportradar.us/motogp/{access_level}/{version}/{language_code}/competitors/{competitor_id}/profile.{return_format}?api_key={your_api_key}
"""



@app.route("/")
def homepage():
	"""Show homepage and all results"""

	results = Result.query.all()
	competitors = Competitor.query.all()
	venues = Venue.query.all()
	return render_template("/homepage.html", 
							competitors=competitors,
							venues=venues)

# import pdb; pdb.set_trace()


################### COMPETITORS PAGES ###########################
### First try at getting just 'Marc Marquez' and storing it as a variable ###
@app.route("/competitors", methods=['GET'])
def competitor_list():
	"""get info from API endpoints, 
	convert from json to python dictionary,
	write to database.

	motogp/trial/v2/en/competitors/:competitor_id/profile:format
	"""
	competitors = Competitor.query.all()
	return render_template('/competitors.html', competitors=competitors)


@app.route("/competitors/<int:competitor_id>")
def competitor_detail(competitor_id):
	"""Show info about specific rider"""

	#some sql alchemy here doing some querying
	competitor = Competitor.query.get(competitor_id)
	teams = Team.query.all()
	results = Result.query.filter_by(competitor_id=competitor_id)

	#SELECT venue_id FROM results WHERE position != N/A

	#select all results in which competitor_id = competitor_id and has a position (not N/A)
	venues = db.session.query(Competitor.competitor_id, Competitor.name)

	return render_template('/competitor.html', 
							competitor=competitor,
							teams=teams, 
							venues=venues,
							results=results)

# @app.route("/competitors/<int:competitor_id>/<int:venue_id>")
# def final_route_detail(competitor_id, venue_id):

# 	competitor = Competitor.query.get(competitor_id)
# 	venue = Venue.query.get(venue_id)

# 	return render_template('/video+map.html',
# 							competitor=competitor)


#################### TEAMS PAGES ################################

@app.route("/teams", methods=['GET'])
def teams_list():
	"""Show list of teams"""

	teams = Team.query.all()
	return render_template('/teams.html', teams=teams)

@app.route("/teams/<team_id>", methods=['GET'])
def team_detail(team_id):
	"""Show info about a specific team"""

	team = Team.query.get(team_id)
	venues = Venue.query.all()

	return render_template('/team.html', team=team, team_id=team_id, venues=venues)




#################### VENUES PAGES ###############################


@app.route("/venues", methods=['GET'])
def venue_list():
	"""Show list of stages in the 2018 Championship"""

	venues = Venue.query.all()
	return render_template('/venues.html', venues=venues)


@app.route("/venues/<int:venue_id>", methods=['GET'])
def venue_detail(venue_id):
	"""Show details about a specific venue"""

	venue = Venue.query.get(venue_id)
	return render_template('/venue.html', venue=venue)


###################### TEST AJAX #################################
@app.route('/order-list.json', methods=['POST'])
def order_list():
	"""Show list of venues that rider has participated at"""

	rider = request.form.get('rider_name')

	if rider == 'marquez':
		venues = Result.query.filter_by(competitor_id =21999)
		result_code = venues
		result_text = 'Here is the list of venues in which Marquez raced at'
	else:
		result_code = 'ERROR'
		result_text = 'Sorry, I didn\'t watch those races'

	return jsonify(venues, {'code': result_code, 'msg': result_text})



@app.route('/rider_results.json', methods=['POST'])
def show_results():
    """Order melons and return a dictionary of result-code and result-msg."""

    competitor = request.form.get("competitor_name")
    venue = request.form.get("venue_name")

    if competitor == 'Marquez, Marc':
    	result_query = Result.query.filter_by(competitor_id=21999)
    	result = result_query(position)



    result_code = 'OK'
    result_text = "You've chosen {}'s results at {}. His finished in {} position".format(competitor, venue, results)

    return jsonify({'code': result_code, 'msg': result_text})












if __name__ == "__main__":

	# app.debug = True

	connect_to_db(app)

	# DebugToolbarExtension(app)
	app.run(host="0.0.0.0")



# <h2>Request Details about Specific Rider</h2>
	
# 	<form id="rider-form">
# 		<div class="form-group">
# 			<label>Rider Name
# 				<select id="rider-name-field" name="rider_name" class="form-control">
# 					<option>marquez</option>
# 					<option>rossi</option>
# 				</select>
# 			</label>
# 		</div>

# 		<div class="form-group">
# 			<button type="submit" id="rider-name-button" class="btn btn-primary">List Details</button>
# 		</div>

# 		<div id="venue-list"></div>



# <script src="http://code.jquery.com/jquery.js"></script>
# <script src="/static/ajax-exercise.js"></script>
