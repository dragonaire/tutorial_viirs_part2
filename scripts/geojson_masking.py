import os
import sh
import json
import rasterio
import shapely.geometry
from affine import Affine
import pandas as pd

import conf


# TODO: this should be scripted to download a file directly to sample_data,
# rather than assuming user has this tif in their local path
#RASTER_FILE = os.path.join(
#    os.path.expanduser('~'), 'bh', 'data', 'satellite',
#    'SVDNB_npp_20140201-20140228_75N180W_vcmcfg_'
#    'v10_c201507201052.avg_rade9.tif'
#)

COUNTIES_GEOJSON_FILE = os.path.join(conf.data_path, 'us_counties_5m.json')
STATE_CODES_FILE = os.path.join(conf.data_path, 'state_codes.txt')

states_df = pd.read_csv(STATE_CODES_FILE, sep='|').set_index('STATE')
states = states_df['STATE_NAME']

with open(COUNTIES_GEOJSON_FILE, 'r') as f:
    counties_raw_geojson = json.load(f, 'latin-1')

def get_county_name_from_geo_obj(geo_obj):
    """
    Use the NAME and STATE properties of a county's geojson
    object to get a name "state: county" for that county.
    """
    return u'{state}: {county}'.format(
        state=states[int(geo_obj['properties']['STATE'])],
        county=geo_obj['properties']['NAME']
    )

counties_geojson = {
    get_county_name_from_geo_obj(county_geojson): county_geojson
    for county_geojson in counties_raw_geojson['features']
}

print len(counties_geojson)
print sorted(counties_geojson.keys())[:10]

