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

class Params:
    """
    Params for retrieving a sample of newcomers for user study recruiting
    """
#output path and snuggle url shouldn't be in criteria
    def __init__(self):
        self.criteria = {
            'curation tools newcomers' : {
                'article edits' : 10,
                'articles edited' : 3,
                'min desirability ratio' : 4.0,
                'from days ago' : 3,
                'to days ago' : 7,
                'days since edit' : 2,
                'max reverts' : 5,
                'skip templates' : ['sock', 'warning', 'block',],
                },                                  
            }
            
        self.queries = {
            'curation tools newcomers' : {
                'email' : 'select user_email from enwiki.user where user_name = "%s";',
                },
            }
            
        self.paths = {
                'curation tools newcomers' : {
                    'file path' : '/home/jmorgan/snuggle_sampling/json/snuggle.json',
                    'snuggle url' : 'http://snuggle-en.wmflabs.org/users/query/%7B%22sorted_by%22:%20%22registration%22,%20%22limit%22:%205000%7D',
                    'output path' : '/home/jmorgan/snuggle_sampling/csv/',
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
        return paths        

