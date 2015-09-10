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

import sampling_config

class Params:
    """
    Params for retrieving a sample of newcomers for user study recruiting
    """
#output path and snuggle url shouldn't be in criteria
    def __init__(self):
        self.criteria = {
            'curation tools newcomers' : {
                'article edits' : 5,
                'articles edited' : 2,
                'min desirability ratio' : 4.0,
                'from days ago' : 3,
                'to days ago' : 7,
                'days since edit' : 2,
                'max reverts' : 2,
                'max mobile edits' : 2,
                'skip templates' : ['sock', 'warning', 'block',],
                },                                  
            }            
        self.queries = {
            'curation tools newcomers' : {
                'email' : 'select user_email from enwiki.user where user_name = "%s";',
                'mobile edits' : 'select count(rc_id) from tag_summary t join recentchanges r on ts_rc_id = rc_id where rc_user_text = "%s" and rc_namespace = 0 and t.ts_tags like "%%mobile edit%%";'
                },
            }
            
        self.paths = {
                'curation tools newcomers' : {
                    'file path' : sampling_config.download_path,
                    'snuggle url' : sampling_config.snuggle_url,
                    'sort field': '{"sorted_by":"registration",',
                    'record limit': '"limit":5000}',
                    'output path' : sampling_config.output_path,
                },
            }   

    def getCriteria(self, sample_type):
        params = self.criteria[sample_type]
        return params   
        
    def getQueries(self, sample_type):
        queries = self.queries[sample_type]
        return queries
        
    def getPaths(self, sample_type):
        paths = self.paths[sample_type]
        paths['api call'] = paths['snuggle url'] + paths['sort field'] + paths['record limit']
        return paths        


