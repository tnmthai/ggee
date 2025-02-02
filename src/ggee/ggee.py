def ee_init(
    token_name="EARTHENGINE_TOKEN",
    auth_mode="notebook",
    service_account=False,
    auth_args={},
    user_agent_prefix="ggee",
    **kwargs,
):
    """Authenticates Earth Engine and initializes an Earth Engine session."""
    import httplib2
    import ee
    import os
    import json
    # from .__init__ import __version__

    user_agent = f"{user_agent_prefix}"
    auth_args["auth_mode"] = auth_mode

    if ee.data._credentials is None:
        ee_token = os.environ.get(token_name)

        if service_account:
            try:
                credential_file_path = os.path.expanduser(
                    "~/.config/earthengine/private-key.json"
                )

                if os.path.exists(credential_file_path):
                    with open(credential_file_path) as f:
                        token_dict = json.load(f)
                    service_account = token_dict["client_email"]
                    private_key = token_dict["private_key"]
                    print(service_account, private_key)
                    credentials = ee.ServiceAccountCredentials(
                        service_account, key_data=private_key
                    )
                    ee.Initialize(credentials, **kwargs)

            except Exception as e:
                raise Exception(e)
 
        else:
            try:
                if ee_token is not None:
                    credential_file_path = os.path.expanduser(
                        "~/.config/earthengine/credentials"
                    )
                    if not os.path.exists(credential_file_path):
                        os.makedirs(
                            os.path.dirname(credential_file_path), exist_ok=True
                        )
                    with open(credential_file_path, "w") as f:
                        f.write(ee_token)
                ee.Initialize(**kwargs)

            except Exception:
                ee.Authenticate(**auth_args)
                ee.Initialize(**kwargs)

    ee.data.setUserAgent(user_agent)

def get_token():
    """Get Earth Engine token.

    Returns:
        dict: The Earth Engine token.
    """
    import os, json

    credential_file_path = os.path.expanduser("~/.config/earthengine/credentials")

    if os.path.exists(credential_file_path):
        with open(credential_file_path, "r") as f:
            credentials = json.load(f)
            return credentials
    else:
        print("Earth Engine credentials not found. Please run ggee.ee_init()")
        return None

def SenL2A(date1, date2, aoi, cpp=100):
    import ee
    Sen2img = ee.ImageCollection('COPERNICUS/S2_SR') \
    .filterDate(date1, date2) \
    .filterBounds(aoi) \
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cpp)) \
    # Get the list of image IDs in the collection.
    image_ids = Sen2img.aggregate_array('system:index').getInfo()

    # Initialize an empty list to store the details.
    image_details = []

    # Iterate over each image ID to get its date and cloud coverage percentage.
    for image_id in image_ids:
        # Get the image corresponding to the current ID.
        img = Sen2img.filter(ee.Filter.eq('system:index', image_id)).first()
        
        # Extract the acquisition date of the image.
        date = img.date().format('yyyy-MM-dd').getInfo()
        
        # Extract the cloud coverage percentage from the image metadata.
        cloud_coverage = img.get('CLOUDY_PIXEL_PERCENTAGE').getInfo()
        
        # Append the details as a tuple to the list.
        image_details.append((date, image_id, cloud_coverage))

    # Now, `image_details` contains all the information.
    print("Date, Image ID, Cloud Coverage")
    for detail in image_details:
        print(detail)
    return image_details

def coordshp(minLon, minLat, maxLon, maxLat, filename="bbox_shapefile.shp"):
    import geopandas as gpd
    from shapely.geometry import Polygon

    # Example bbox coordinates
    bbox = [[minLon, minLat], [maxLon, maxLat]]

    # Convert bbox to Polygon
    polygon = Polygon([(bbox[0][0], bbox[0][1]), (bbox[1][0], bbox[0][1]), (bbox[1][0], bbox[1][1]), (bbox[0][0], bbox[1][1])])

    # Create a GeoDataFrame
    gdf = gpd.GeoDataFrame(index=[0], crs='EPSG:4326', geometry=[polygon])

    # Export to Shapefile
    gdf.to_file(filename)
