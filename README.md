<ol>
    <li>
        <ul>
            <li><strong>Get all locations</strong></li>
            <li><strong>URL:</strong> /api/locations</li>
            <li><strong>Method:</strong> GET</li>
            <li><strong>Description:</strong> Retrieves data for all locations.</li>
        </ul>
    </li>
    <li>
        <ul>
            <li><strong>Get location by postal code</strong></li>
            <li><strong>URL:</strong> /api/locations/pcode</li>
            <li><strong>Method:</strong> GET</li>
            <li><strong>Description:</strong> Retrieves location data for the specified postal code.</li>
        </ul>
    </li>
    <li>
        <ul>
            <li><strong>Get locations by state/region</strong></li>
            <li><strong>URL:</strong> /api/locations/stateregions/&lt;stateregion&gt;</li>
            <li><strong>Method:</strong> GET</li>
            <li><strong>Description:</strong> Retrieves location data for the specified state or region.</li>
        </ul>
    </li>
    <li>
        <ul>
            <li><strong>Get locations by township</strong></li>
            <li><strong>URL:</strong> /api/locations/townships/&lt;stateregion&gt;</li>
            <li><strong>Method:</strong> GET</li>
            <li><strong>Description:</strong> Retrieves location data for the specified township.</li>
        </ul>
    </li>
    <li>
        <ul>
            <li><strong>Calculate distance between two locations</strong></li>
            <li><strong>URL:</strong> /api/calculate-distance?latitude1=22&amp;longitude1=89&amp;longitude2=80&amp;latitude2=30</li>
            <li><strong>Method:</strong> GET</li>
            <li><strong>Description:</strong> Calculates the distance between two locations specified by latitude and longitude.</li>
            <li><strong>Parameters:</strong>
                <ul>
                    <li>latitude: Latitude of the reference location.</li>
                    <li>longitude: Longitude of the reference location.</li>
                </ul>
            </li>
        </ul>
    </li>
    <li>
        <ul>
            <li><strong>Get nearest location from the dataset</strong></li>
            <li><strong>URL:</strong> /api/nearest-location?latitude=22&amp;longitude=89</li>
            <li><strong>Method:</strong> GET</li>
            <li><strong>Description:</strong> Retrieves the nearest location from the dataset based on the specified latitude and longitude.</li>
            <li><strong>Parameters:</strong>
                <ul>
                    <li>latitude1: Latitude of the first location.</li>
                    <li>longitude1: Longitude of the first location.</li>
                    <li>latitude2: Latitude of the second location.</li>
                    <li>longitude2: Longitude of the second location.</li>
                </ul>
            </li>
        </ul>
    </li>
</ol>
