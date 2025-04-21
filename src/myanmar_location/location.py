import json
from math import radians, sin, cos, acos, asin, sqrt
import csv
import os
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

# https://en.wikipedia.org/wiki/Haversine_formula
# haversine distance: 2*r*arcsin(sqrt(1-cos(phi2-phi1)+cosphi1*cosphi2*(1-cos(lambda2-lambda1))/2))

# arithmetic mean radius of Earth in miles
radius_ml = 3958.7613

# arithmetic mean radius of Earth in km
radius_km = 6371.0088

def calculate_distance(location1, location2):     
    lat1 = radians(location1[0])
    lon1 = radians(location1[1])
    lat2 = radians(location2[0])
    lon2 = radians(location2[1])   
   
    d = acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon1 - lon2))
    d_ml = radius_ml * d
    d_km = radius_km * d
    return d_ml, d_km
    
def get_nearest_location(location):
    nearest_distance_ml = nearest_distance_km = 0
    nearest_location = None    
    data = read_file()   
    count = -1
    # Loop through the rows and calculate the distance
    for row in data:
        count = count + 1

        # Skip if the location is INACTIVE or has no coordinates
        if row["IsActive"] == 0 or row["Longitude"] == '' or row["Latitude"] == '':
            continue

        # Convert latitude/longitude to float
        longitude = float(row["Longitude"])
        latitude = float(row["Latitude"])

        # Calculate the distance
        distance_ml, distance_km = calculate_distance(location, [latitude, longitude])  
         
        # Compare the new and previous calculated distances and insert the shorter location into nearest_location. 
        if nearest_distance_ml == 0 or nearest_distance_ml > distance_ml:
            nearest_location = row
            nearest_distance_ml = distance_ml
            nearest_distance_km = distance_km
   
    # Append calculated distance
    nearest_location['DistanceInKM'] = nearest_distance_km
    nearest_location['DistanceInMile'] = nearest_distance_ml
    
    # Remove unimportant data points
    # remove_fields(nearest_location, ["Source","StartDate","ModifiedEndDate","Notification","NotificationModified","GADVillageStatus",
    #                     "FieldVillageStatus","MIMUVillageMappingStatus","ChangeType","MIMURemarks","Type","Remarks","IsActive"])
    
    print(nearest_location)
    return nearest_location

def convert_float(value):
    try:
        return float(value)        
    except Exception:
        return None
 
def remove_fields(dictionary, fields_to_remove):
    for field in fields_to_remove:
        if field in dictionary:
            del dictionary[field]
    return dictionary

def read_file(file_name = 'mimu9.4.csv'):
    # Get the current directory
    current_dir = os.getcwd()
    
    # Join Location file path
    file_path = os.path.join(current_dir, file_name)
    
    # read the file
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
    
    # Set the last page number if page_number is greater than total pages
    # page_number = total_pages if page_number > total_pages else page_number   

    # Return an empty list if page_number is greater than the last page number.
    if page_number > total_pages:
        return [] 
        
    # Calculate start and end indices for the current page
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    
    # Slice the data
    result = data[start_index:end_index]
    
    return result    
    
# Define routes
# All locations
@app.route('/api/locations', methods=['GET'])
def get_locations():    
    stateregion = request.args.get('stateregion')
    district = request.args.get('district')
    township = request.args.get('township')
    villagetracttown = request.args.get('villagetracttown')
    villageward = request.args.get('villageward')
    locations = read_file()
    if stateregion:
        locations = [l for l in locations if l["StateRegion"].lower() == stateregion.lower().strip()]
    if district:
        locations = [l for l in locations if l["District"].lower() == district.lower().strip()]
    if township:
        locations = [l for l in locations if l["Township"].lower() == township.lower().strip()]
    if villagetracttown:
        locations = [l for l in locations if l["VillageTractTown"].lower() == villagetracttown.lower().strip()]
    if villageward:
        locations = [l for l in locations if l["LocationName"].lower() == villageward.lower().strip()]
        
    result = slice_data(locations, request.args.get('page_number'), request.args.get('page_size'))
    if result:
        return jsonify({"locations":result})
    else:
        return jsonify({'message': 'Locations not found.'}), 404

# Location by PCode
@app.route('/api/locations/<string:pcode>', methods=['GET'])
def get_location(pcode):
    locations = read_file()
    location = next((location for location in locations if location['LocationPCode'] == pcode), None)
    if location:
        return jsonify({"location":location})
    else:
        return jsonify({'message': 'Location not found.'}), 404    
 
# Get State/Regions
@app.route('/api/locations/stateregions', methods=['GET'])
def get_stateregions():    
    stateregions = read_file('mimu_stateregion.csv')
    stateregion = request.args.get('stateregion')
    if stateregion:
        stateregions = [s for s in stateregions if s["StateRegion"].lower() == stateregion.lower().strip()]
    result = slice_data(stateregions, request.args.get('page_number'), request.args.get('page_size'))    
    if result:
        return jsonify({"stateregions":result})
    else:
        return jsonify({'message': 'State/regions not found.'}), 404
    
# Get Districts    
@app.route('/api/locations/districts', methods=['GET'])
def get_districts():    
    districts = read_file('mimu_district.csv')
    district = request.args.get('district')
    if district:
        districts = [t for t in districts if t["District"].lower() == district.lower().strip()]
    result = slice_data(districts, request.args.get('page_number'), request.args.get('page_size'))    
    if result:
        return jsonify({"districts":result})
    else:
        return jsonify({'message': 'Districts not found.'}), 404

# Get Townships    
@app.route('/api/locations/townships', methods=['GET'])
def get_townships(): 
    townships = read_file('mimu_township.csv')
    township = request.args.get('township')
    if township:
        townships = [t for t in townships if t["Township"].lower() == township.lower().strip()]
    result = slice_data(townships, request.args.get('page_number'), request.args.get('page_size'))    
    if result:
        return jsonify({"townships":result})
    else:
        return jsonify({'message': 'Townships not found.'}), 404
  
# Get VillageTract/Towns    
@app.route('/api/locations/villagetracttowns', methods=['GET'])
def get_villagetracts():    
    villagetracttowns = read_file('mimu_villagetract.csv')
    villagetracttown = request.args.get('villagetracttown')
    if villagetracttown:
        villagetracttowns = [v for v in villagetracttowns if v["VillageTractTown"].lower() == villagetracttown.lower().strip()]
    result = slice_data(villagetracttowns, request.args.get('page_number'), request.args.get('page_size'))    
    if result:
        return jsonify({"villagetracttowns":result})
    else:
        return jsonify({'message': 'Village tracts or towns not found.'}), 404
 
# Get Nearest Location in the location dataset
@app.route('/api/locations/nearest-location', methods=['GET'])
def nearest_location():
    latitude = convert_float(request.args.get('latitude'))
    longitude = convert_float(request.args.get('longitude'))
    
    if latitude is None:
        return jsonify({'message': 'Please provide a valid decimal number for the latitude of the reference location.'}), 400
    if longitude is None:
        return jsonify({'message': 'Please provide a valid decimal number for the longitude of the reference location.'}), 400
    try:
        location =  get_nearest_location([latitude,longitude])
        if location:
            return jsonify({"NearestLocation":location})
        else:
            return jsonify({'message': 'Location not found.'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': e}), 400

# Calculate the distance between two locations
@app.route('/api/calculate-distance', methods=['GET'])
def get_distance():
    latitude1 = convert_float(request.args.get('latitude1'))
    longitude1 = convert_float(request.args.get('longitude1'))
    latitude2 = convert_float(request.args.get('latitude2'))
    longitude2 = convert_float(request.args.get('longitude2'))
    
    if latitude1 is None or longitude1 is None or latitude2 is None or longitude2 is None:
        return jsonify({'message': 'Please provide all coordinates, and all must be valid decimal numbers.'}), 400
    
    try:
        distance =  calculate_distance([latitude1,longitude1], [latitude2,longitude2])
        return {"distance_in_mile": distance[0], "distance_in_km": distance[1]}
    except ValueError as e:
        print(e)
        return jsonify({'message': e}), 400
    except Exception as e:
        print(e)
        return jsonify({'message': e}), 400

if __name__ == '__main__':    
    app.run(port=5000)
    # app.run(debug=True)
