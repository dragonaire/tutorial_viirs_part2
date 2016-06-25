# VIIRS Tutorial
How to use the VIIRS satellite data for night time lights.

## Setup:
`pip install -r requirements.txt`

## To Do:
https://docs.google.com/document/d/1f9YrGHhNkstJyN5mgjLaYcULEvsaLpOD5M-yHJZhIqA/edit#heading=h.wbn2cx2bqdh5

##

1. Download the data.

   Try
   ```
   python scripts/download_viirs_data.py -h
   ```
   to see how to use the script.

   As an example, to download only February data in North America:
   ```
   python scripts/download_viirs_data.py --months=2 --tiles=75N180W --outfolder=viirs_data --live
   ```
