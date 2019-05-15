from sqlalchemy import func
from model import Competitor, Team, Result, Venue, Season
from model import connect_to_db, db 
from flask import Flask, jsonify, request
import requests
from flask_restless import APIManager
from flask import Flask, render_template, flash, redirect

#using api lab "balloonicorn's party" from hackbright as example

app = Flask(__name__)
app.secret_key = "NOTSUREYETBUTOKAY"

sportradar_token = 

# url_template = https://api.sportradar.us/motogp/{access_level}/{version}/{language_code}/competitors/{competitor_id}/profile.{format}?api_key={your_api_key}

sportradar_url = "http://api.sportradar.us/motogp/trial/v2/en/"


@app.route("/")
def homepage():
	"""Show homepage"""

	return render_template("homepage.html")


@app.route("/competitor")
def competitors():
	"""Show list of all competitors"""

	return render_template("cometitors.html")




















if __name__ == '__main__':
	connect_to_db(app)

	manager = APIManager(app, flask_sqlalchemy_db=db)

	# Create API endpoints, which will be available at /api/<tablename> by default. Allowed HTTP methods can be specified as well.

	manager.create_api(
		Competitor,
		methods = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])

	manager.create_api(
		Team,
		methods = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])

	manager.create_api(
		Result,
		methods = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])

	manager.create_api(
		Venue,
		methods = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])

	manager.create_api(
		Season,
		methods = ['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
