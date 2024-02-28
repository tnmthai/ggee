# Earth Engine Initialization Library

This library provides a set of functions to authenticate and initialize Google Earth Engine (EE) sessions, retrieve EE tokens, and query Sentinel-2 image data. It supports both service account-based and token-based authentication, making it suitable for a wide range of EE applications.

## Features

- **EE Session Initialization**: Authenticate and initialize an EE session using either a service account or a personal account token.
- **Token Retrieval**: Retrieve an EE token from a local file for subsequent EE operations.
- **Sentinel-2 Image Query**: Query Sentinel-2 images by date range and area of interest (AOI), with details about each image's acquisition date and cloud coverage.

## Installation

Before using this library, ensure you have the Earth Engine Python API installed. You can install it using pip:

```bash
pip install earthengine-api
```

## Usage
### Initializing Earth Engine

```bash
from ggee import *

# Initialize EE without service account (token-based authentication)
ee_init()

# Initialize EE with service account
ee_init(service_account=True)
```
### Retrieving Earth Engine Token


```bash
from your_library_name import get_token

# Retrieve and print the EE token
token = get_token()
print(token)
```

### Querying Sentinel-2 Images


```bash
from ggee import SenL2A
import ee

# Define your area of interest (AOI)
aoi = ee.Geometry.Rectangle([minLon, minLat, maxLon, maxLat])

# Query Sentinel-2 images
image_details = SenL2A('2021-01-01', '2021-01-31', aoi)

# Print image details
for detail in image_details:
    print(detail)
```
## Contributing
Contributions to this library are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.