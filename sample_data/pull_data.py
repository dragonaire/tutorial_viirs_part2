# Pull the data you see here in sample_data, which is used in the tutorial
import sh

urls = {
    'us_counties_5m.json' : 'http://eric.clst.org/wupl/Stuff/gz_2010_us_050_00_5m.json',
    'state_codes.txt': 'http://www2.census.gov/geo/docs/reference/state.txt'
}

for name, url in urls.iteritems():
    print 'Pull data for {} from {}'.format(name, url)
    sh.curl(url, o=name, silent=True)

