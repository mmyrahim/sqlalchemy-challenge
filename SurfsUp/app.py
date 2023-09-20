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
        "/api/v1.0/precipitation - Precipitation data for the last year<br/>"
        "/api/v1.0/stations - List of weather stations<br/>"
        "/api/v1.0/tobs - Temperature observations for the most active station (last year)<br/>"
    )

# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # create a new session
    session = create_session()
    
    # calculate the date one year from the last date in the dataset
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_prior = most_recent_date - dt.timedelta(days=365)
    
    # query and format precipitation data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_prior).all()
    
    # close the session
    session.close()
    
    # convert the results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    
    return jsonify(precipitation_data)

# stations route
@app.route("/api/v1.0/stations")
def stations():
    # create a new session
    session = create_session()
    
    # query and format station data
    results = session.query(Station.station).all()
    
    # close the session
    session.close()
    
    # convert the results to a list
    station_data = [station for station, in results]
    
    return jsonify(station_data)

# TOBS route
@app.route("/api/v1.0/tobs")
def tobs():
    # create a new session
    session = create_session()
    
    # calculate the date one year from the last date in the dataset
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_prior = most_recent_date - dt.timedelta(days=365)
    
    # query and format temperature observations
    results = session.query(Measurement.tobs).filter(Measurement.station == "USC00519281").filter(Measurement.date >= one_year_prior).all()
    
    # close the session
    session.close()
    
    # convert the results to a list
    tobs_data = [tobs for tobs, in results]
    
    return jsonify(tobs_data)

# run the app
if __name__ == "__main__":
    app.run(debug=True)