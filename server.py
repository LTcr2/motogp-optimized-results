"""MotoGP Results."""

from jinja2 import StrictUndefined
from flask import Flask, jsonify, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import Competitor, Team, Result, Venue, connect_to_db, db

import requests
import json

from sqlalchemy import func

#using api lab "balloonicorn's party" from hackbright as example

######################## SPORT RADAR API INITIALIZATION #################
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

"""
Endpoint format:

https://api.sportradar.us/motogp/{access_level}/{version}/{language_code}/competitors/{competitor_id}/profile.{return_format}?api_key={your_api_key}
"""


######################## YOUTUBE API INITIALIZATION ####################
@app.route("/")
def titlepage():

	return render_template("/title.html")

@app.route("/homepage")
def homepage():
	"""Show homepage and all results"""

	results = Result.query.all()
	competitors = Competitor.query.all()
	venues = Venue.query.all()

	#pseudocode
	#do a youtube search with the form keywords and limitations
	#get json response
	#pick out the video_id from json responses
	#store video_id
	#pass video_id to the homepage.html



	return render_template("/homepage.html", 
							competitors=competitors,
							venues=venues)

# import pdb; pdb.set_trace()



###################### AJAX #################################

@app.route('/rider_results.json', methods=['POST'])
def show_results():
    """Order melons and return a dictionary of result-code and result-msg."""

    #getting the selected rider and venue from the form on the page
    select_competitor = request.form.get("competitor_name")
    select_venue = request.form.get("venue_description")

    #COOL TOOL!
    print(request.values.to_dict())
    # print(select_competitor)
    # print(select_venue)

    #query the results using the selected competitor name and venue name selected
    	#first find the competitor_id with the competitor's name
    	#or just get that as the entry? maybe refactor later

    #find the object of both competitor and venue based on the name we got from the form
    competitor_object = Competitor.query.filter_by(name=select_competitor).first()
    venue_object = Venue.query.filter_by(description=select_venue).first()

    #first the ID of both competitor_object and venue_id
    competitor_id = competitor_object.competitor_id
    venue_id = venue_object.venue_id

    competitor_name = competitor_object.name


    #find the results of that competitor at that venue
    select_result = Result.query.filter_by(competitor_id=competitor_id, venue_id=venue_id).first()

    #get the position the rider ended with
    position = select_result.position

    #if the rider earned a position as an integer, print P(number)

    if position == 'C':
    	result_text = "Race was cancelled due to weather conditions."
    	result_code = 'OK'
    elif position == 'DNS':
    	result_text = "Rider did not start(DNS)."
    	result_code = 'OK'
    elif position == 'N/A':
    	result_text = "Rider did not participate in at this stage."
    	result_code = 'OK'
    elif position == 'WD':
    	result_text = "Rider withdrew."
    	result_code = 'OK'
    elif position == 'R':
    	result_text = "Rider was retired."
    	result_code = 'OK'
    else:
	    result_text = "You've chosen {}'s results at {}. Rider finished in {} position.".format(select_competitor, select_venue, position)
	    result_code = 'OK'

    return jsonify({'code': result_code, 'msg': result_text})





@app.route('/youtube_results.json', methods=['POST'])
def show_youtube():
    
    select_competitor = request.form.get("competitor_name")
    select_venue = request.form.get("venue_description")
    select_order = request.form.get("sort_by")
    select_numresults = request.form.get("num_results")
    print(request.values.to_dict())


    developer_key = 'AIzaSyB-zKkfLXp_xVgmsNPO7QF41uEQ0Dl2x6Y'

    
    # hardcode_example = "https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q=valentino%20rossi&key="+developer_key


    formatted_keywords = select_competitor+ " "+select_venue
    print(formatted_keywords)

    url = "https://www.googleapis.com/youtube/v3/search"

    payload = {'part': 'snippet',
    		   'maxResults': select_numresults,
    		   'q': formatted_keywords,
    		   'key':'AIzaSyB-zKkfLXp_xVgmsNPO7QF41uEQ0Dl2x6Y'}


    response = requests.get(url, params=payload)

    data = response.json()

    print(data)


    return jsonify(data)



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

	# import pdb; pdb.set_trace()

	#some sql alchemy here doing some querying
	competitor = Competitor.query.get(competitor_id)


	# team_id = Team.query.filter_by(competitor_id=competitor_id)
	results = Result.query.filter_by(competitor_id=competitor_id)


	#SELECT venue_id FROM results WHERE position != N/A

	#select all results in which competitor_id = competitor_id and has a position (not N/A)
	results = Result.query.filter_by(competitor_id=competitor_id).all()

	venue_ids = []
	for result in results:
		venue_ids.append(result.venue_id)
	#now venue_ids have a list of all the venues in which this competitor


	#this lists all the venue_ids and the position the rider finished at
	venue_position_dict = {}
	for result in results:
		venue_position_dict[result.venue_id] = result.position


	venues = []
	for venue_id in venue_ids:
		venue_object = Venue.query.filter_by(venue_id=venue_id).first()
		venues.append(venue_object)



	return render_template('/competitor.html',
							venue_position_dict=venue_position_dict, 
							competitor=competitor, 
							venues=venues,
							results=results)

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

	return render_template('/team.html', team=team, 
										 team_id=team_id, 
										 venues=venues)

#################### VENUES PAGES ###############################


@app.route("/venues", methods=['GET'])
def venue_list():
	"""Show list of stages in the 2018 Championship"""

	venues = Venue.query.all()
	return render_template('/venues.html', venues=venues)


@app.route("/venues/<int:venue_id>", methods=['GET'])
def venue_detail(venue_id):
	"""Show details about a specific venue"""

	developer_key = 'AIzaSyBLAgXE42atlvCmAIJopHRVLe08v9MyAaM'

	cota = "https://www.google.com/maps/embed/v1/view?zoom=15&center=30.1385%2C-97.6353&key=AIzaSyBLAgXE42atlvCmAIJopHRVLe08v9MyAaM"

	venue = Venue.query.get(venue_id)
	lat = venue.latitude
	lon = venue.longitude

	payload = {'developer_key': developer_key,
			 'longitude': venue.longitude,
			 'latitude': venue.latitude}


	return render_template('/venue.html', venue=venue)

################### ABOUT #######################################

@app.route('/about')
def show_about():

	return render_template('about.html')









if __name__ == "__main__":

	app.debug = True

	connect_to_db(app)

	# DebugToolbarExtension(app)
	app.run(host="0.0.0.0", port=5001)



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
