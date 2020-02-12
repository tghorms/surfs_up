import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement 
Station = Base.classes.station 

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
     """List all available api routes."""
     return (
         f"Available Routes:<br/>"
         f"/api/v1.0/precipitation<br/>"
         f"/api/v1.0/stations<br/>"
         f"/api/v1.0/tobs<br/>"
         f"/api/v1.0/<i>enter_start<i><br/>"
         f"/api/v1.0/<i>enter_start<i>/<i>enter_end<i>"

     )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date = max_date[0]
    # Calculate the date 1 year ago from the last data point in the database

    last_year = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=366)

    # Perform a query to retrieve the data and precipitation scores
    results_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()

    precipitation_dict = dict(results_prcp)

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    """List all available weather stations."""

    # Perform a query to retrieve stations.
    results_stations = session.query(Measurement.station).group_by(Measurement.station).all()

    stations_list = list(np.ravel(results_stations))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """query for the dates and temperature observations from a year from the last data point."""
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date = max_date[0]
    last_year = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=366)

    # Perform a query to retrieve dates and tobs from a year from last data point.
    results_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= last_year).all()
    tobs_list = list(results_tobs)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start=None):
    """list of the minimum temperature, the average temperature, and the max temperature for a given start"""
    start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date == start).group_by(Measurement.date).all()
    start_date_list = list(start_date)

    # all_temps = []
    # for tmin, tavg, tmax in start_date:
    #         temps_dict = {}
    #         temps_dict["tmin"] = tmin
    #         temps_dict["tavg"] = tavg
    #         temps_dict["tmax"] = tmax
    #         all_temps.append(temps_dict)
    return jsonify(start_date_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    """list of the minimum temperature, the average temperature, and the max temperature for a given start-end range"""
    date_range = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    date_range_list = list(date_range)
    return jsonify(date_range_list)



if __name__ == '__main__':
    app.run(debug=True)
