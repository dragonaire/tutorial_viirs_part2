# Downloading viirs data

We've created a script [download_viirs_data.py](scripts/download_viirs_data.py)
to make downloading viirs data easy.

Try
```
python scripts/download_viirs_data.py -h
```
to see how to use the script.

As an example, to download only February data in North America:
```
python scripts/download_viirs_data.py --months=2 --tiles=75N180W --outfolder=data/viirs --live
```
