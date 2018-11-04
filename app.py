import numpy as np

import datetime as dt
from datetime import date, timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
app = Flask(__name__)

#################################################
# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes are as follows:<br/>"
        f"<br>"
        f"Returns a list dates and precipitation information from the last 12 months:<br>"
        f"  /api/v1.0/precipitation<br/>"
        f"<br>"
        f"Returns a list of stations from the dataset<br>"
        f"  /api/v1.0/stations<br/>"
        f"<br>"
        f"Returns dates and temperature observations from a year from the last data point:<br>"
        f"  /api/v1.0/tobs<br/>"
        f"<br>"
        f"Insert start and end date to return the minimum temperature, the average temperature, and the max temperature for date duration.<br>"
        f"If single date is entered then result will return the min max and average for that date and all the dates that follow.<br>"
        f"  /api/v1.0/start date/end date<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list dates and precipitation information from the last 12 months"""
    # Query 12 months of precipitation and return values in dictionary format
    yrAgo = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    percip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= yrAgo).all()
    percip_dict=dict(percip)
    return jsonify(percip_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    # Query 12 months of precipitation and return values in dictionary format
    stations = session.query(Station.station).all()
    station_lsit = list(np.ravel(stations))
    return jsonify(station_lsit)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return dates and temperature observations from a year from the last data point"""
    # Query 12 months of precipitation and return values in dictionary format
    yrAgo = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= yrAgo).all()
    temps_dict=dict(temps)
    return jsonify(temps_dict)

@app.route("/api/v1.0/<start>/<end>")
def trip_temps(start,end):
    """Return minimum temperature, the average temperature, and the max temperature for a given start or start-end"""
    if end != None:
        min_avg_max = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:   
        min_avg_max = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).all()

    return jsonify(min_avg_max)


if __name__ == '__main__':
    app.run(debug=True)