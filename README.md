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
