import csv
import importlib.resources as pkg_resources
from math import acos, cos, radians, sin
from typing import Any

from flask import Flask

from . import RADIUS_KM, RADIUS_ML
from . import data as _data_resources
from ._types import Location

app = Flask(__name__)


def calculate_distance(location1: Location, location2: Location):
    """
    https://en.wikipedia.org/wiki/Haversine_formula
    Haversine distance: 2*r*arcsin(sqrt(1-cos(phi2-phi1)+cosphi1*cosphi2*(1-cos(lambda2-lambda1))/2))
    """
    lat1 = radians(location1.lat)
    lon1 = radians(location1.lon)
    lat2 = radians(location2.lat)
    lon2 = radians(location2.lon)

    d = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))
    d_ml = RADIUS_ML * d
    d_km = RADIUS_KM * d
    return d_ml, d_km


def get_nearest_location(location: Location):
    nearest_distance_ml = nearest_distance_km = 0
    nearest_location = None
    data = read_file()
    count = -1
    # Loop through the rows and calculate the distance
    for row in data:
        count = count + 1

        # Skip if the location is INACTIVE or has no coordinates
        if row["IsActive"] == 0 or row["Longitude"] == "" or row["Latitude"] == "":
            continue

        # Convert latitude/longitude to float
        longitude = float(row["Longitude"])
        latitude = float(row["Latitude"])

        # Calculate the distance
        distance_ml, distance_km = calculate_distance(
            location, Location(lat=latitude, lon=longitude)
        )

        # Compare the new and previous calculated distances and insert the shorter location into nearest_location.�
        if nearest_distance_ml == 0 or nearest_distance_ml > distance_ml:
            nearest_location = row
            nearest_distance_ml = distance_ml
            nearest_distance_km = distance_km

    # Append calculated distance
    if nearest_location:
        nearest_location["DistanceInKM"] = nearest_distance_km
        nearest_location["DistanceInMile"] = nearest_distance_ml

    # Remove unimportant data points
    # remove_fields(nearest_location, ["Source","StartDate","ModifiedEndDate","Notification","NotificationModified","GADVillageStatus",
    #                     "FieldVillageStatus","MIMUVillageMappingStatus","ChangeType","MIMURemarks","Type","Remarks","IsActive"])

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


def read_file(file_name="mimu9.4.csv") -> list[dict[str | Any, str | Any]]:
    dir_path = pkg_resources.files(_data_resources)
    file_path = dir_path / file_name
    with file_path.open("r") as file:
        csv_reader = csv.DictReader(file)
        data = list(csv_reader)
        return data


def slice_data(data, page_number, page_size):
    # If there is no or an invalid page_number/page_size, set the default value.
    page_number = (
        1 if page_number == None or not page_number.isdigit() else int(page_number)
    )
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
