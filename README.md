# VIIRS Tutorial
How to use the VIIRS satellite data for night time lights.

## Setup:
`pip install -r requirements.txt`

## Using VIIRS data

1. **Downloading data**

   Before you can use VIIRS data do do anything interesting, you must [download the VIIRS data](download_data.md).

1. **Working with data**

   After downloading the data, you'll surely want to do something interesting with it.
   We have written [a tutorial](geo_json.md) with examples of how to look at data for particular geographical regions,
   as a starting point.

   We would love to see people explore things like:
  - Find counties with the most change in light data, see how it correlates with other growth metrics
  - More generally, see how metrics such as population and income relate to light data
  - Look into World Bank ICP/PPP, population, and infrastructure data.
    Areas with low PPP, high population density, and recent infrastructure grants should show corresponding increase in NTL (night time lights).
    If this is not the case, could it be potential fraud?

1. **Visualizing data**

   We also have an example of an [end-to-end website](https://github.com/bayeshack2016/sysj/tree/master/site)
   that lets you visualize VIIRS data (and other county data) for different counties and time periods,
   by imposing the data a map.

