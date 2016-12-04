
# Working with GeoJSON data

## Obtaining GeoJSON data

You can find GeoJSON data for the United states [here](http://eric.clst.org/Stuff/USGeoJSON)

For example, to download county-level data at medium resolution:
```
curl http://eric.clst.org/wupl/Stuff/gz_2010_us_050_00_5m.json -o data/us_counties_5m.json
```

## Combining GeoJSON data with VIIRS data

We've written a function [load_raster_with_mask](scripts/geojson_masking.md)
which takes a raster file and GeoJSON mask, and outputs the masked data.

There's also a [short tutorial](nb/Geojson and Rasterio Demo.ipynb)
explaining how it works and how to use it.
