from datastories.app import app, db
from flask import request, url_for, flash, redirect, session, render_template, jsonify
from sqlalchemy.sql import func
from datastories.models.weather import Location, Forecast
from .utils import get_coordinates, get_forecast
from statistics import mean, median
import plotly.graph_objs as gs


@app.route('/', methods=['GET'])
def home():    
    locations = Location.query.all()
    
    temp_data = []
    for obj in locations:
        for item in obj.weather:
            results = {
                "location": obj.name,
                "period": item.period,
                "min_temp": item.min_temp,
                "max_temp": item.max_temp,
                "humidity": item.humidity,
                "average": obj.avg_temp,
                "median": obj.median_temp
            }
            temp_data.append(results)
            
    data = {(obj["location"], obj["average"]): obj for obj in temp_data}
    result = list(data.values()) 
            
    if not result:
        return jsonify({'status': 'error', 'message': 'No data found.'}), 404
    
    x = [data['location'] for data in result]
    y = [data['average'] for data in result]
    cities = [data['location'] for data in result]
    
    data = gs.Bar(x=x, y=y)
    layout = gs.Layout(title=f'Average Temperature for overall cities: {cities}')
    figure = gs.Figure(data=[data], layout=layout)
    
    chart_json = figure.to_json()
    
    return render_template('index.html', chart=chart_json)



@app.route('/api/weather', methods=['POST'])
def create_weather_data():
    """API route for getting weather data and saves to the database.

    Args: 
        params: Takes in location (string) and period (int) 
    Returns:
        JSON: A response with the min, max, avg & median in JSON 
    """
    location_coord = ''
    forecast_data = {}
    med = ''
    avg = ''
    new_location = None
    
    data = request.get_json()
    location = data['location']
    period = data['period']
    
    if request.method == 'POST':
        if location and period:
            # Call util function to get coordinates from mapbox api
            location_coord = get_coordinates(location)
            lat = location_coord[1]
            lon = location_coord[0]
            
            forecast_data = get_forecast(lat, lon, period, location)
            
            # Get the Average and Median
            lst = [[item["max"], item["min"]] for item in forecast_data["forecast"]]
            flatList = [element for innerList in lst for element in innerList]

            avg = round(mean(flatList), 2)
            med = round(median(flatList), 2)
            
            # Updated the dictionary with average and median keys
            forecast_data['average'] = avg
            forecast_data['median'] = med
            
            if bool(forecast_data):
                # Save data to db
                new_location = Location(
                                name=forecast_data["location"],
                                avg_temp=forecast_data["average"],
                                median_temp=forecast_data["median"],
                    )
                
                qs = []
                for item in forecast_data["forecast"]:
                    forecast = Forecast(
                        period=item["date"],
                        min_temp=item["min"],
                        max_temp=item["max"],
                        humidity=item["humidity"],
                        forecasts=new_location
                    )
                    qs.append(forecast)
                db.session.add(new_location)
                db.session.add_all(qs)
                db.session.commit()
                
            return jsonify({"status": "success", "data": forecast_data}), 201
        else:
            return jsonify({"error": "Please make sure a location and period are entered!"}), 400
