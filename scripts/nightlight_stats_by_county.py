import os
import argparse
import numpy as np
import json
import rasterio
import pandas as pd
from geojson_masking import load_raster_with_mask

sample_data_dir = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'sample_data')

counties_geojson_file = os.path.join(
    sample_data_dir, 'us_counties_5m.json')

state_codes_file = os.path.join(
    sample_data_dir, 'state_codes.txt')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''Compute night light statistics for US counties''',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '--raster_file',
        type=str,
        help='raster file for satellite data',
    )
    parser.add_argument(
        '--output_file',
        type=str,
        help='path for output csv with night light statistics',
    )

    args = parser.parse_args()
    raster_file = rasterio.open(args.raster_file, 'r')

    with open(counties_geojson_file, 'r') as f:
        counties_raw_geojson = json.load(f, 'latin-1')

    states_df = pd.read_csv(state_codes_file, sep='|').set_index('STATE')
    states = states_df['STATE_NAME']

    def get_county_name_from_geo_obj(geo_obj):
        """
        Use the NAME and STATE properties of a county's geojson
        object to get a name "state: county" for that county.
        """
        return u'{state}: {county}'.format(
            state=states[int(geo_obj['properties']['STATE'])],
            county=geo_obj['properties']['NAME']
        )

    # rearrange the raw geojson so the keys are county names with states
    counties_geojson = {
        get_county_name_from_geo_obj(county_geojson): county_geojson
        for county_geojson in counties_raw_geojson['features']
    }

    def get_nightlights_stats(county_name, county_geojson, raster_file):
        '''
        Calculate the mean, median, and standard deviation
        '''
        masked_nightlights = load_raster_with_mask(
            raster_file,
            county_geojson['geometry']
        )
        return {'county_name': county_name,
                'mean': np.ma.mean(masked_nightlights),
                'median': np.ma.median(masked_nightlights),
                'std': np.ma.std(masked_nightlights),
                }

    county_satellite_data = [
        get_nightlights_stats(county_name, county_geojson, raster_file)
        for county_name, county_geojson in counties_geojson.iteritems()
    ]

    df = pd.DataFrame.from_records(county_satellite_data, index='county_name')
    df.to_csv(args.output_file)
