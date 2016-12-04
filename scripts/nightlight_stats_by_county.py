import os
import argparse
import numpy as np
import json
import rasterio
import rasterio.features
import pandas as pd
from geojson_masking import load_raster_with_mask

sample_data_dir = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'sample_data')

counties_geojson_file = os.path.join(
    sample_data_dir, 'us_counties_5m.json')

state_codes_file = os.path.join(
    sample_data_dir, 'state_codes.txt')

def get_counties_geojson(counties_geojson_file, state_codes_file):
    with open(counties_geojson_file, 'r') as f:
        counties_raw_geojson = json.load(f, 'latin-1')

    states_df = pd.read_csv(state_codes_file, sep='|').set_index('STATE')
    states = states_df['STATE_NAME']

    # rearrange the raw geojson so the keys are county names with states
    counties_geojson = {
        get_county_name_from_geo_obj(county_geojson): county_geojson
        for county_geojson in counties_raw_geojson['features']
    }
    return counties_geojson

def get_county_name_from_geo_obj(geo_obj):
    """
    Use the NAME and STATE properties of a county's geojson
    object to get a name "state: county" for that county.
    """
    return u'{state}: {county}'.format(
        state=states[int(geo_obj['properties']['STATE'])],
        county=geo_obj['properties']['NAME']
    )

def masked_median(masked_data):
    """
    Get the median of a masked array. This function is needed because
    np.ma.median returns differently shaped output depending on whether
    any data is masked.

    (This behavior is odd, and not clear at all from the docs)
    """
    np_ma_median = np.ma.median(masked_data)
    if np_ma_median.data.shape == ():
        return np.float(np_ma_median.data)
    else:
        return np_ma_median.data[0]

def get_nightlights_stats(county_name, county_geojson, rasterio_file):
    '''
    Calculate the mean, median, and standard deviation
    '''
    masked_nightlights = load_raster_with_mask(
        rasterio_file,
        county_geojson['geometry']
    )
    # NOTE: np.ma.median returns a 1x1 masked array, so we get the
    # actual median by indexing `data`
    return {'county_name': county_name,
            'mean': np.ma.mean(masked_nightlights),
            'median': masked_median(masked_nightlights),
            'std': np.ma.std(masked_nightlights),
            }

def get_stats(counties_geojson, raster_file, output_file):
    rasterio_file = rasterio.open(raster_file, 'r')

    county_satellite_data = [
        get_nightlights_stats(county_name, county_geojson, rasterio_file)
        for county_name, county_geojson in counties_geojson.iteritems()
    ]

    df = pd.DataFrame.from_records(county_satellite_data, index='county_name')
    df.to_csv(output_file, encoding='utf-8')
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='''
        Compute night light statistics for US counties

        Given a raster file and the counties geojson in sample_data, write
        out a csv with columns:
            county_name, mean, median, std
        for each U.S. county, where county_name is in 'State: County' format
        ''',
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

    counties_geojson = get_counties_geojson(counties_geojson_file, state_codes_file):
    df = get_stats(counties_geojson, args.raster_file, args.output_file)
    print df.head()

