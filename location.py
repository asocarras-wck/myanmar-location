import json
from math import radians, sin, cos, acos, asin, sqrt
import csv
import os
from flask import Flask, request, jsonify
app = Flask(__name__)

# https://en.wikipedia.org/wiki/Haversine_formula
# haversine distance: 2*r*arcsin(sqrt(1-cos(phi2-phi1)+cosphi1*cosphi2*(1-cos(lambda2-lambda1))/2))

# arithmetic mean radius of Earth in miles
radius_ml = 3958.7613

# arithmetic mean radius of Earth in km
radius_km = 6371.0088

# Get the current directory
current_dir = os.getcwd()
    
# Join Location file path
file_path = os.path.join(current_dir, 'myanmar_location\\mimu9.4.csv')

def calculate_distance(location1, location2):     
    lat1 = radians(location1[0])
    lon1 = radians(location1[1])
    lat2 = radians(location2[0])
    lon2 = radians(location2[1])   
   
    d = acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon1 - lon2))
    d_ml = radius_ml * d
    d_km = radius_km * d
    return d_ml, d_km

def remove_fields(dictionary, fields_to_remove):
    for field in fields_to_remove:
        if field in dictionary:
            del dictionary[field]
    return dictionary
    
def get_nearest_location(location):
    nearest_distance_ml = nearest_distance_km = 0
    nearest_location = None    
    csv_reader = read_file()   
    count = -1
    # Loop through the rows and calculate distance
    for row in csv_reader:
        count = count + 1

        # Skip if the location is INACTIVE or has no coordinates
        if row["IsActive"] == 0 or row["Longitude"] == '' or row["Latitude"] == '':
            continue

        # Get latitude/longitude from the file
        longitude = float(row["Longitude"])
        latitude = float(row["Latitude"])

        # Construct the UPDATE query
        distance_ml, distance_km = calculate_distance(location, [latitude, longitude])  
                
        if nearest_distance_ml == 0 or nearest_distance_ml > distance_ml:
            nearest_location = row
            nearest_distance_ml = distance_ml
            nearest_distance_km = distance_km
   
    # Append calculated distance
    nearest_location['DistanceInKM'] = nearest_distance_km
    nearest_location['DistanceInMile'] = nearest_distance_ml
    
    # Remove unnecessary data points
    # remove_fields(nearest_location, ["Source","StartDate","ModifiedEndDate","Notification","NotificationModified","GADVillageStatus",
    #                     "FieldVillageStatus","MIMUVillageMappingStatus","ChangeType","MIMURemarks","Type","Remarks","IsActive"])
    
    print(nearest_location)
    return nearest_location
        
def read_file():
    with open(file_path, 'r', encoding = "utf8") as file:   
        csv_reader = csv.DictReader(file)  
        data = list(csv_reader)
        return data    
    
def slice_data(data, page_number, page_size):
    # If there is no or an invalid page_number/page_size, set the default value.
    page_number = 1 if page_number == None or not page_number.isdigit() else int(page_number)
    page_size = 200 if page_size == None or not page_size.isdigit() else int(page_size)
    
    # Calculate the number of pages in the dataset
    total_pages = (len(data) + page_size - 1) // page_size
    
    # Set the max page number if page_number is greater than total pages
    page_number = total_pages if page_number > total_pages else page_number   
        
    # Calculate start and end indices for the current page
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    
    # Slice the data
    result = data[start_index:end_index]
    
    return result    
    
# Define routes
@app.route('/api/locations', methods=['GET'])
def get_locations():    
    locations = read_file()
    result = slice_data(locations, request.args.get('page_number'), request.args.get('page_size'))
    return jsonify(result)

@app.route('/api/locations/<string:pcode>', methods=['GET'])
def get_location(pcode):
    locations = read_file()
    location = next((location for location in locations if location['VillagePCode'] == pcode), None)
    if location:
        return jsonify({"location":location})
    else:
        return jsonify({'message': 'Location not found'}), 404    

@app.route('/api/locations/stateregions/<string:stateregion>', methods=['GET'])
def get_location_by_stateregion(stateregion):
    locations = read_file()
    match_locations = []
    for location in locations:
        if location['StateRegion'].lower() == stateregion.lower():
            match_locations.append(location)
            
    result = slice_data(match_locations, request.args.get('page_number'), request.args.get('page_size'))
    if result:
        return jsonify({"locations":result})
    else:
        return jsonify({'message': 'Location not found'}), 404   
    
@app.route('/api/locations/townships/<string:township>', methods=['GET'])
def get_locations_by_township(township):    
    locations = read_file()
    match_locations = []
    for location in locations:
        if location['Township'].lower() == township.lower():
            match_locations.append(location)
            
    result = slice_data(match_locations, request.args.get('page_number'), request.args.get('page_size'))
    if result:
        return jsonify({"locations":result})
    else:
        return jsonify({'message': 'Location not found'}), 404
    
@app.route('/api/nearest-location', methods=['GET'])
def nearest_location():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    location =  get_nearest_location([latitude,longitude])
    if location:
        return jsonify({"NearestLocation":location})
    else:
        return jsonify({'message': 'Location not found'}), 404

@app.route('/api/calculate-distance', methods=['GET'])
def get_distance():
    latitude1 = float(request.args.get('latitude1'))
    longitude1 = float(request.args.get('longitude1'))
    latitude2 = float(request.args.get('latitude2'))
    longitude2 = float(request.args.get('longitude2'))    
    try:
        distance =  calculate_distance([latitude1,longitude1], [latitude2,longitude2])
        return {"distance_in_mile": distance[0], "distance_in_km": distance[1]}
    except ValueError as e:
        print(e)
        return jsonify({'message': e}), 400

@app.route('/')
def hello():
    return """
        <h1>Myanmar Locations API</h1>
        <div>This is a simple Flask-based RESTful API project that provides functionality for retrieving village and ward-level locations in Myanmar, 
        finding the nearest location within the dataset, and additionally, calculating the distance between two locations. 
        The dataset is sourced from the <a href='https://themimu.info/place-codes'>Myanmar Information Management Unit (MIMU)</a>, with data stored in a CSV file serving as the database.</div>
        <h2>Endpoints</h2>
        <ol>       
    <li>
	<strong>Get all locations</strong>
	<ul>
            <li>URL: /api/locations</li>
            <li>Method: GET</li>
            <li>Description: Retrieves data for all locations.</li>
        </ul>
    </li>
    <li>       
        <strong>Get location by postal code</strong>
	<ul>
            <li>URL: /api/locations/pcode</li>
            <li>Method: GET</li>
            <li>Description: Retrieves location data for the specified postal code.</li>
        </ul>
    </li>
    <li>
        <strong>Get locations by state/region</strong>
	<ul>
            <li>URL: /api/locations/stateregions/&lt;stateregion&gt;</li>
            <li>Method: GET</li>
            <li>Description: Retrieves location data for the specified state or region.</li>
        </ul>
    </li>
    <li>
        <strong>Get locations by township</strong>
	<ul>
            <li>URL: /api/locations/townships/&lt;stateregion&gt;</li>
            <li>Method: GET</li>
            <li>Description: Retrieves location data for the specified township.</li>
        </ul>
    </li>    
     <li>        
        <strong>Calculate distance between two locations</strong>
	<ul>
            <li>URL: /api/calculate-distance</li>
            <li>Method: GET</li>
            <li>Description: Calculates the distance between two locations specified by latitude and longitude.</li>
            <li>Parameters:
                <ul>
                    <li>latitude1: Latitude of the first location.</li>
                    <li>longitude1: Longitude of the first location.</li>
                    <li>latitude2: Latitude of the second location.</li>
                    <li>longitude2: Longitude of the second location.</li>
                </ul>
            </li>
        </ul>
    </li>
    <li>
        <strong>Get nearest location from the dataset</strong>
	<ul>            
            <li>URL: /api/nearest-location</li>
            <li>Method: GET</li>
            <li>Description: Retrieves the nearest location from the dataset based on the specified latitude and longitude.</li>
            <li>Parameters:
                <ul>
		    <li>latitude: Latitude of the reference location.</li>
                    <li>longitude: Longitude of the reference location.</li>                    
                </ul>
            </li>
        </ul>
    </li>
</ol>
    """

if __name__ == '__main__':    
    app.run(port=5000)
    # app.run(debug=True)
