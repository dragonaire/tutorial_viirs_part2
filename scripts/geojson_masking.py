from affine import Affine
import rasterio
import shapely.geometry
import numpy as np


def load_raster_with_mask(raster_file, geojson_geometry):
    """
    Given a rasterio file and a geojson geometry, return a
    numpy masked array of pixel values for coordinates within
    that geometry.

    Typically the geojson geometry is under the 'geometry' key of
    a geojson feature.

    You can recover the pixel values for the entire bounding box by
    accessing the `data` field of the masked array, or the mask
    itself by accessing the `mask` field.

    """
    # get the bounding box, as latitude and longitude
    geo_shape = shapely.geometry.shape(geojson_geometry)
    lon_min, lat_min, lon_max, lat_max = geo_shape.bounds
    # get the bounding box as indices of the raster file
    # (note that the order of coordinates gets flipped here,
    #  the first index is for latitude, the second for longitude)
    bottom, left = raster_file.index(lon_min, lat_min)
    top, right = raster_file.index(lon_max, lat_max)
    raster_window = ((top, bottom+1), (left, right+1))
    # load the raw pixel data for the bounding box as a 2d array
    bounding_box_array = raster_file.read(indexes=1, window=raster_window)
    # create an updated affine mapping. Slicing into the bounding box
    # did not change the scaling or rotation of pixels, but the offset
    # changed.
    rfa = raster_file.affine
    bounding_box_affine = Affine(
        rfa.a, rfa.b, lon_min,
        rfa.d, rfa.e, lat_max
    )
    # now that we know the affine mapping, we can use rasterio.rasterize
    # to find which pixels fall inside the geojson geometry. In the first
    # argument, we are saying we want 0 wherever we fall inside the geo
    # shape, and the `fill` argument is specifying that we get 1 outside.
    # This is because numpy uses this convention for masked data.
    inclusion_mask = rasterio.features.rasterize(
        shapes=[(geo_shape, 0)],
        out_shape=bounding_box_array.shape,
        transform=bounding_box_affine,
        fill=1,
        dtype=np.uint8,  # this is the smallest available dtype
    )
    # create the masked array
    masked_data = np.ma.array(
        data=bounding_box_array,
        mask=inclusion_mask,
    )
    return masked_data
