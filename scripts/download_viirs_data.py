"""
This script scrapes the NOAA website to download viirs data
"""

import argparse
from argparse import RawTextHelpFormatter
from bs4 import BeautifulSoup
import os
import requests
import sh

BASE_URL = 'http://mapserver.ngdc.noaa.gov/viirs_data/viirs_composite/v10'

# list a directory on the website
def list_path(path):
    r = requests.get(BASE_URL + path)
    parsed_html = BeautifulSoup(r.text, "lxml")
    rows = parsed_html.body.find('table').find_all('tr')

    # ignore first three rows, and last row
    rows = rows[3:-1]

    result = []
    for row in rows:
        href = row.find("a").attrs['href']
        if href is not None:
            result.append(href)
    return result

def get_time_periods():
    return [
        x[:-1] for x in
        list_path('/')
        if x.endswith('/')
    ]

def parse_time_period(time_period):
    year = int(time_period[:4])
    month = int(time_period[4:])
    return (year, month)

def parse_tile_filename(tile_file):
    parts = tile_file.split('_')
    tile = parts[3]
    return tile

def get_tile_files(time_period):
    # paths = list_path('/%s' % time_period)
    # assert paths == ['vcmcfg/', 'vcmslcfg/']
    paths = list_path('/%s/vcmcfg' % time_period)
    # ignores the png files
    return [path for path in paths if path.endswith('.tgz')]

def download_data(output_folder, tiles=None, years=None, months=None, live=True):
    for time_period in get_time_periods():
        (year, month) = parse_time_period(time_period)
        if not (months is None or month in months):
            continue # not a month we care about
        if not (years is None or year in years):
            continue # not a year we care about
        for tile_file in get_tile_files(time_period):
            tile = parse_tile_filename(tile_file)
            if not (tiles is None or tile in tiles):
                continue # not a tile we care about
            url = '%s/%s/vcmcfg/%s' % (BASE_URL, time_period, tile_file)
            if live:
                # 'Warning: files to be downloaded are large'
                sh.tar(
                    sh.curl(url, _piped=True),
                    "xzv",
                    _cwd=output_folder
                )
            else:
                print 'Would download %s' % url
    if not live:
        print """
        Use --live to actually download!'
        Warning: files are large (about 2G each)
        """

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
    Download VIIRS data from the viirs website.

    For example, to download only February data in North America:
    python download_viirs_data.py --months=2 --tiles=75N180W --outfolder=viirs_data --live

    For more flexibility, you can also use this as a library.  See the implementation of
    download_data to get a sense

    """, formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        '--months',
        type=str,
        help='a comma separated list of months, e.g. 1,6 (defaults to all)',
        default=None,
    )
    parser.add_argument(
        '--years',
        type=str,
        help='a comma separated list of years, e.g. 2013,2014 (defaults to all)',
        default=None,
    )
    parser.add_argument(
        '--tiles',
        type=str,
        help="""
        A comma separated list of tiles.
        Valid tiles:
        75N180W : tile 1, north america
        75N060W : tile 2
        75N060E : tile 3
        00N180W : tile 4
        00N060W : tile 5
        00N060E : tile 6
        """,
        default=None,
    )
    parser.add_argument(
        '--live',
        type=bool,
        help="Whether to actually download",
        default=False,
    )
    parser.add_argument(
        '--outfolder',
        type=str,
        help="Which folder to download data to",
        default='viirs_data',
    )

    args = parser.parse_args()

    months = None if args.months is None else map(int, filter(len, args.months.split(',')))
    years =  None if args.years  is None else map(int, filter(len, args.years.split(',') ))
    tiles =  None if args.tiles  is None else filter(len, args.tiles.split(',') )

    sh.mkdir('-p', args.outfolder)
    download_data(
        args.outfolder,
        tiles=tiles,
        years=years,
        months=months,
        live=args.live,
    )
