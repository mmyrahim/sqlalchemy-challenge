# import necessary libraries and dependencies
from flask import Flask, jsonify
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# create a Flask app
app = Flask(__name__)

# create an engine to connect to your SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the database schema
Base = automap_base()
Base.prepare(engine, reflect=True)

# reflect the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# function to create and return a new database session
def create_session():
    return Session(engine)

# landing page
@app.route("/")
def home():
    return (
        "Welcome to the Climate Analysis API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation - Precipitation data 