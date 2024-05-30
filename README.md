<h1>Myanmar Locations API</h1>
    <div>
        This is a simple RESTful API project that provides functionality for retrieving Myanmar location data, including village/ward, village tract/town, township, district, and state/region information.
        Additionally, it offers features for finding the nearest location within the dataset and calculating the distance between two geographic locations.
        The dataset is sourced from the <a href='https://themimu.info/place-codes'>Myanmar Information Management Unit (MIMU)</a>, with data stored in a CSV file serving as the database.
    </div>    
    <h2>Endpoints</h2>
    <ol>
        <li>
            <strong>Get all locations</strong>
            <ul>
                <li>URL: /api/locations</li>
                <li>Method: GET</li>
                <li>Description: Retrieves data for all village and ward-level locations.</li>
                <li>
                    Parameters:
                    <ul>
                        <li>stateregion (optional): Filter locations by state/region.</li>
                        <li>district (optional): Filter locations by district.</li>
                        <li>township (optional): Filter locations by township.</li>
                        <li>villagetracttown (optional): Filter locations by village tract/town.</li>
                        <li>page_number (optional): Page number for pagination (default is 1).</li>
                        <li>page_size (optional): Number of locations per page (default is 200).</li>
                    </ul>
                </li>
                <li>
                    Response:
                    <ul>
                        <li>200 OK: Returns a JSON object containing a list of locations.</li>
                        <li>404 Not Found: If no locations match the specified postal code.</li>
                    </ul>
                </li>
            </ul>
        </li>
        <li>
            <strong>Get Location by PCode (postal code)</strong>
            <ul>
                <li>URL: /api/locations/<string:pcode></li>
                <li>Method: GET</li>
                <li>Description: Retrieves location data for the specified postal code.</li>
                <li>
                    Path Parameter:
                    <ul>
                        <li>pcode: PCode of the location.</li>
                    </ul>
                </li>
                <li>
                    Response:
                    <ul>
                        <li>200 OK: Returns a JSON object containing a location.</li>
                        <li>404 Not Found: If no location match the specified postal code.</li>
                    </ul>
                </li>
            </ul>
        </li>
        <li>
            <strong>Get State/Regions</strong>
            <ul>
                <li>URL: /api/locations/stateregions</li>
                <li>Method: GET</li>
                <li>Description: Retrieves a list of state/regions.</li>
                <li>
                    Parameters:
                    <ul>
                        <li>stateregion (optional): Filter state/regions by name.</li>
                        <li>page_number (optional): Page number for pagination (default is 1).</li>
                        <li>page_size (optional): Number of state/regions per page (default is 200).</li>
                    </ul>
                </li>
                <li>
                    Response:
                    <ul>
                        <li>200 OK: Returns a JSON object containing a list of state/regions.</li>
                        <li>404 Not Found: If no state/regions match the specified criteria.</li>
                    </ul>
                </li>
            </ul>
        </li>
        <li>
            <strong>Get Districts</strong>
            <ul>
                <li>URL: /api/locations/districts</li>
                <li>Method: GET</li>
                <li>Description: Retrieves a list of districts.</li>
                <li>
                    Parameters:
                    <ul>
                        <li>district (optional): Filter districts by name.</li>
                        <li>page_number (optional): Page number for pagination (default is 1).</li>
                        <li>page_size (optional): Number of districts per page (default is 200).</li>
                    </ul>
                </li>
                <li>
                    Response:
                    <ul>
                        <li>200 OK: Returns a JSON object containing a list of districts.</li>
                        <li>404 Not Found: If no districts match the specified criteria.</li>
                    </ul>
                </li>
            </ul>
        </li>
        <li>
            <strong>Get Townships</strong>
            <ul>
                <li>URL: /api/locations/townships</li>
                <li>Method: GET</li>
                <li>Description: Retrieves a list of townships.</li>
                <li>
                    Parameters:
                    <ul>
                        <li>township (optional): Filter townships by name.</li>
                        <li>page_number (optional): Page number for pagination (default is 1).</li>
                        <li>page_size (optional): Number of townships per page (default is 200).</li>
                    </ul>
                </li>
                <li>
                    Response:
                    <ul>
                        <li>200 OK: Returns a JSON object containing a list of townships.</li>
                        <li>404 Not Found: If no townships match the specified criteria.</li>
                    </ul>
                </li>
            </ul>
        </li>
        <li>
            <strong>Get Village Tract/Towns</strong>
            <ul>
                <li>URL: /api/locations/villagetracttowns</li>
                <li>Method: GET</li>
                <li>Description: Retrieves a list of villagetracttowns.</li>
                <li>
                    Parameters:
                    <ul>
                        <li>villagetracttown (optional): Filter village tract/towns by name.</li>
                        <li>page_number (optional): Page number for pagination (default is 1).</li>
                        <li>page_size (optional): Number of village tract/towns per page (default is 200).</li>
                    </ul>
                </li>
                <li>
                    Response:
                    <ul>
                        <li>200 OK: Returns a JSON object containing a list of village tract/towns.</li>
                        <li>404 Not Found: If no village tract/towns match the specified criteria.</li>
                    </ul>
                </li>
            </ul>
        </li>
        <li>
            <strong>Get nearest location from the dataset</strong>
            <ul>
                <li>URL: /api/locations/nearest-location</li>
                <li>Method: GET</li>
                <li>Description: Retrieves the nearest location from the dataset based on the specified latitude and longitude.</li>
                <li>
                    Parameters:
                    <ul>
                        <li>latitude: Latitude of the reference location.</li>
                        <li>longitude: Longitude of the reference location.</li>
                    </ul>
                </li>
                <li>
                    Response:
                    <ul>
                        <li>200 OK: Returns a JSON object containing the nearest location.</li>
                        <li>404 Not Found: If no location match the specified criteria.</li>
                    </ul>
                </li>
            </ul>
        </li>
        <li>
            <strong>Calculate distance between two locations</strong>
            <ul>
                <li>URL: /api/calculate-distance</li>
                <li>Method: GET</li>
                <li>Description: Calculates the distance between two geographic locations specified by latitude and longitude.</li>
                <li>
                    Parameters:
                    <ul>
                        <li>latitude1: Latitude of the first location.</li>
                        <li>longitude1: Longitude of the first location.</li>
                        <li>latitude2: Latitude of the second location.</li>
                        <li>longitude2: Longitude of the second location.</li>
                    </ul>
                </li>
                <li>
                    Response:
                    <ul>
                        <li>200 OK: Returns a JSON object containing the distance between the two coordinates in both miles and kilometers.</li>
                        <li>400 Bad Request: If there's an error, it returns a 400 Bad Request with an error message.</li>
                    </ul>
                </li>
            </ul>
        </li>
    </ol>