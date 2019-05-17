from sqlalchemy import func
from model import Competitor, Team, Result, Venue
from model import connect_to_db, db 
from flask import Flask, jsonify, request
import requests
from flask import Flask, render_template, flash, redirect
import json
# from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined


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



"""
Endpoint format:

https://api.sportradar.us/motogp/{access_level}/{version}/{language_code}/competitors/{competitor_id}/profile.{return_format}?api_key={your_api_key}
"""



@app.route("/")
def homepage():
	"""Show homepage"""

	return render_template("/homepage.html")



### First try at getting just 'Marc Marquez' and storing it as a variable ###
@app.route("/get-competitor-name", methods=['GET'])
def get_competitor_name():
	"""get info from API endpoints, 
	convert from json to python dictionary,
	write to database.

	motogp/trial/v2/en/competitors/:competitor_id/profile:format
	"""

	url = "http://api.sportradar.us/motogp/trial/v2/en/competitors/sr:competitor:21999/profile.json?api_key=t2pxakdxpkskhr3ajc3rgb72"
 	

	headers = {'Authorization': 'Bearer' + your_api_key}

	response = requests.get(url)

	data = response.json()
	print(data['schema'])

	competitor_name = data['competitor']


	return render_template('/competitor_profile.html')

@app.route("/competitor-profile/<int:competitor_id>")
def show_comp_profile():

	return render_template('/competitor_profile.html', competitor=competitor)















if __name__ == "__main__":

	# app.debug = True

	connect_to_db(app)

	# DebugToolbarExtension(app)

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
