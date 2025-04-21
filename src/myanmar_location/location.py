from flask import Flask, jsonify, request

from .utils import (
    calculate_distance,
    convert_float,
    get_nearest_location,
    read_file,
    slice_data,
)

app = Flask(__name__)

# https://en.wikipedia.org/wiki/Haversine_formula
# haversine distance: 2*r*arcsin(sqrt(1-cos(phi2-phi1)+cosphi1*cosphi2*(1-cos(lambda2-lambda1))/2))


# Define routes
# All locations
@app.route("/api/locations", methods=["GET"])
def get_locations():
    stateregion = request.args.get("stateregion")
    district = request.args.get("district")
    township = request.args.get("township")
    villagetracttown = request.args.get("villagetracttown")
    villageward = request.args.get("villageward")
    locations = read_file()
    if stateregion:
        locations = [
            l
            for l in locations
            if l["StateRegion"].lower() == stateregion.lower().strip()
        ]
    if district:
        locations = [
            l for l in locations if l["District"].lower() == district.lower().strip()
        ]
    if township:
        locations = [
            l for l in locations if l["Township"].lower() == township.lower().strip()
        ]
    if villagetracttown:
        locations = [
            l
            for l in locations
            if l["VillageTractTown"].lower() == villagetracttown.lower().strip()
        ]
    if villageward:
        locations = [
            l
            for l in locations
            if l["LocationName"].lower() == villageward.lower().strip()
        ]

    result = slice_data(
        locations, request.args.get("page_number"), request.args.get("page_size")
    )
    if result:
        return jsonify({"locations": result})
    else:
        return jsonify({"message": "Locations not found."}), 404


# Location by PCode
@app.route("/api/locations/<string:pcode>", methods=["GET"])
def get_location(pcode):
    locations = read_file()
    location = next(
        (location for location in locations if location["LocationPCode"] == pcode), None
    )
    if location:
        return jsonify({"location": location})
    else:
        return jsonify({"message": "Location not found."}), 404


# Get State/Regions
@app.route("/api/locations/stateregions", methods=["GET"])
def get_stateregions():
    stateregions = read_file("mimu_stateregion.csv")
    stateregion = request.args.get("stateregion")
    if stateregion:
        stateregions = [
            s
            for s in stateregions
            if s["StateRegion"].lower() == stateregion.lower().strip()
        ]
    result = slice_data(
        stateregions, request.args.get("page_number"), request.args.get("page_size")
    )
    if result:
        return jsonify({"stateregions": result})
    else:
        return jsonify({"message": "State/regions not found."}), 404


# Get Districts
@app.route("/api/locations/districts", methods=["GET"])
def get_districts():
    districts = read_file("mimu_district.csv")
    district = request.args.get("district")
    if district:
        districts = [
            t for t in districts if t["District"].lower() == district.lower().strip()
        ]
    result = slice_data(
        districts, request.args.get("page_number"), request.args.get("page_size")
    )
    if result:
        return jsonify({"districts": result})
    else:
        return jsonify({"message": "Districts not found."}), 404


# Get Townships
@app.route("/api/locations/townships", methods=["GET"])
def get_townships():
    townships = read_file("mimu_township.csv")
    township = request.args.get("township")
    if township:
        townships = [
            t for t in townships if t["Township"].lower() == township.lower().strip()
        ]
    result = slice_data(
        townships, request.args.get("page_number"), request.args.get("page_size")
    )
    if result:
        return jsonify({"townships": result})
    else:
        return jsonify({"message": "Townships not found."}), 404


# Get VillageTract/Towns
@app.route("/api/locations/villagetracttowns", methods=["GET"])
def get_villagetracts():
    villagetracttowns = read_file("mimu_villagetract.csv")
    villagetracttown = request.args.get("villagetracttown")
    if villagetracttown:
        villagetracttowns = [
            v
            for v in villagetracttowns
            if v["VillageTractTown"].lower() == villagetracttown.lower().strip()
        ]
    result = slice_data(
        villagetracttowns,
        request.args.get("page_number"),
        request.args.get("page_size"),
    )
    if result:
        return jsonify({"villagetracttowns": result})
    else:
        return jsonify({"message": "Village tracts or towns not found."}), 404


# Get Nearest Location in the location dataset
@app.route("/api/locations/nearest-location", methods=["GET"])
def nearest_location():
    latitude = convert_float(request.args.get("latitude"))
    longitude = convert_float(request.args.get("longitude"))

    if latitude is None:
        return jsonify(
            {
                "message": "Please provide a valid decimal number for the latitude of the reference location."
            }
        ), 400
    if longitude is None:
        return jsonify(
            {
                "message": "Please provide a valid decimal number for the longitude of the reference location."
            }
        ), 400
    try:
        location = get_nearest_location([latitude, longitude])
        if location:
            return jsonify({"NearestLocation": location})
        else:
            return jsonify({"message": "Location not found."}), 404
    except Exception as e:
        print(e)
        return jsonify({"message": e}), 400


# Calculate the distance between two locations
@app.route("/api/calculate-distance", methods=["GET"])
def get_distance():
    latitude1 = convert_float(request.args.get("latitude1"))
    longitude1 = convert_float(request.args.get("longitude1"))
    latitude2 = convert_float(request.args.get("latitude2"))
    longitude2 = convert_float(request.args.get("longitude2"))

    if (
        latitude1 is None
        or longitude1 is None
        or latitude2 is None
        or longitude2 is None
    ):
        return jsonify(
            {
                "message": "Please provide all coordinates, and all must be valid decimal numbers."
            }
        ), 400

    try:
        distance = calculate_distance([latitude1, longitude1], [latitude2, longitude2])
        return {"distance_in_mile": distance[0], "distance_in_km": distance[1]}
    except ValueError as e:
        print(e)
        return jsonify({"message": e}), 400
    except Exception as e:
        print(e)
        return jsonify({"message": e}), 400


if __name__ == "__main__":
    app.run(port=5000)
    # app.run(debug=True)
