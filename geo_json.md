
# Working with GeoJSON data

## Obtaining GeoJSON data

You can find GeoJSON data for the United states [here](http://eric.clst.org/Stuff/USGeoJSON)

That file will indicate states using numeric codes instead of names.
See [here](http://www2.census.gov/geo/docs/reference/state.txt) for conversion between codes and names.

We've written [a short script](sample_data/pull_data.py) to download the aforementioned data for you,
in a manner useable for the rest of this tutorial.

## Combining GeoJSON data with VIIRS data

We've written a function [load_raster_with_mask](scripts/geojson_masking.py)
which takes a raster file and GeoJSON mask, and outputs the masked data.

There's also a [short tutorial](nb/Geojson and Rasterio Demo.ipynb)
explaining how it works and how to use it to compute some basic statistics.
