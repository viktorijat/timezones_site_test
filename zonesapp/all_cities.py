import os
from collections import defaultdict
from datetime import datetime
from urllib import urlretrieve
from urlparse import urljoin
from zipfile import ZipFile
import pytz


def get_city_info(given_city):

    geonames_url = 'http://download.geonames.org/export/dump/'
    basename = 'cities15000' # all cities with a population > 15000 or capitals
    filename = basename + '.zip'

    if not os.path.exists(filename):
        urlretrieve(urljoin(geonames_url, filename), filename)

    city2tz = defaultdict(set)
    with ZipFile(filename) as zf, zf.open(basename + '.txt') as file:
        for line in file:
            fields = line.split(b'\t')
            if fields:
                name, asciiname, alternatenames = fields[1:4]
                timezone = fields[-2].decode('utf-8').strip()
                if timezone:
                    for city in [name, asciiname] + alternatenames.split(b','):
                        city = city.decode('utf-8').strip()
                        if city:
                            city2tz[city].add(timezone)

    #print("Number of available city names (with aliases): %d" % len(city2tz))
    #print city2tz
    n = sum((len(timezones) > 1) for city, timezones in city2tz.iteritems())
    #print("")
    #print("Find number of ambigious city names\n "
    #      "(that have more than one associated timezone): %d" % n)

    fmt = '%Y-%m-%d %H:%M:%S %Z%z'

    print "given_city", given_city
    if given_city in city2tz:
        information = []
        for tzname in city2tz[given_city]:
            now = datetime.now(pytz.timezone(tzname))
            now2 = datetime.now(pytz.timezone("GMT"))
            datetime_now = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
            datetime_gmt = datetime(now2.year, now2.month, now2.day, now2.hour, now2.minute, now2.second)

            if datetime_gmt > datetime_now:
                difference = datetime_gmt - datetime_now
            else:
                difference = datetime_now - datetime_gmt

            #print "diff", difference
            #print("%s is in %s timezone" % (given_city, tzname))
            #print("Current time in %s is %s" % (given_city, now.strftime(fmt)))

            info = [str(difference), now.strftime(fmt), tzname]
            information.append(info)

        return information

    else:
        return False
