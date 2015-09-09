#! /usr/bin/python2.7

# Copyright 2015 Jtmorgan

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import calendar
import json
import urllib2
from datetime import datetime
from datetime import timedelta

class Download:
    """
    Params for retrieving a sample of newcomers from Snuggle for user study recruiting
    """

    def __init__(self, snuggle_url, file_path):
#     def __init__(self, file_path):

        """define the API URL and the local file path"""
        print snuggle_url
        proxy = urllib2.ProxyHandler({'http': 'webproxy.eqiad.wmnet:8080'})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        self.data = urllib2.urlopen(snuggle_url)
        self.path = file_path
        
    def downloadData(self):
        """download JSON from Snuggle API"""
        local_data = open(self.path, 'w')
        local_data.write(self.data.read())
        local_data.close()
        
    def convertJSON(self):
        """convert JSON to dict"""
        d = open(self.path)
        json_data = json.load(d)
        d.close()
        
        return json_data    
    
    def filterDataByDate(self, sample_datetime, days_from, days_to, days_ago, raw_data):
        """filter items by date"""
        date_from = sample_datetime-timedelta(days=days_from)
        print date_from
        date_to = sample_datetime-timedelta(days=days_to)
        print date_to
        date_ago = sample_datetime-timedelta(days=days_ago)
        df_unix = calendar.timegm(date_from.timetuple()) #merge
        dt_unix = calendar.timegm(date_to.timetuple()) #merge
        da_unix = calendar.timegm(date_ago.timetuple()) #merge

        filtered_data = [x for x in raw_data if x['registration'] < df_unix and x['registration'] > dt_unix and x['activity']['last_activity'] > da_unix]
        
        return filtered_data


        
        
        
        
        
        
        
        
        
        