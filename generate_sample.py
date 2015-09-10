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

from datetime import datetime #move to data?
from datetime import timedelta #move to data?
import csv
import data
import MySQLdb
import parameters
import sampling_config
import sys
from warnings import filterwarnings

# 1. get a sample of users from Snuggle
# - calculate begin and end params to grab from
# 2. filter by
# - non-reverted edits to main namespace
# - common talkpage warning messages
# - desirability ratio/score
# - number of articles edited
# latest activity threshold


def countArticleEdits(u):
    edits = 0
    if '0' in u['activity']['counts']:
        edits = u['activity']['counts']['0']
    return edits

def countArticles(u):
    articles = 0
    article_titles = []
    for k,v in u['activity']['revisions'].iteritems():
        if v['page']['namespace'] == 0:
            article_titles.append(v['page']['title'])
    if len(article_titles) > 0:
        article_titles = set(article_titles)
        articles = len(article_titles)
    return articles

# def countReverts():
def isWarned(u):
    warned = False
    if u['has_talk_page'] == True:
        threads = u['talk']['threads']
        if len(threads) > 0:
            for t in threads:
                if t['trace']:
                    if t['trace']['name']:
                        if "warning" in t['trace']['name']:
                            warned = True
                        elif "block" in t['trace']['name']:
                            warned = True    
    return warned                            

def countMobileEdits(u, criteria, db):
    mostly_mobile = False
    mobile_edits = db.getUserData('mobile edits', u['name'])
    if type(mobile_edits) is str:
        pass
    elif mobile_edits > criteria['max mobile edits']:
        mostly_mobile = True
    return mostly_mobile    
  
        
def makeSample(user_data, criteria, db):
    #if desirability ratio is working, use it. if not, don't.
    user_data = [x for x in user_data if x['desirability']['ratio'] > criteria['min desirability ratio']] 
    user_list = []    
    for u in user_data:
#         try:
        article_edits = countArticleEdits(u)
        articles = countArticles(u)
        warned = isWarned(u)
        mostly_mobile = countMobileEdits(u, criteria, db)
#             if article_edits >= 10 and articles >= 2 and not warned:

        if article_edits >= 5 and articles >= 2 and not warned and not mostly_mobile:
                user_list.append({'username':u['name'], 'contribs':'https://en.wikipedia.org/wiki/Special:Contributions/' + u['name']})
#             print u['desirability']['ratio']        
#         except:
#             pass
#     print user_list        
    return user_list
            
def getEmails(user_list, db):
    for u in user_list:
        email = db.getUserData('email', u['username'])
        u['email'] = email            
    user_list_emails = [x for x in user_list if len(x['email']) > 0]
    return user_list_emails   
    
    
def createSampleFile(user_list, sample_datetime):
    filename = str(sample_datetime.strftime('%Y%m%d%H%M%S')) + ".csv" #use datetime instead?
    path = paths['output path']
    with open(path + filename, 'w') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow( ('user name', 'contribs link', 'email') )
        for u in user_list:
            try:
                writer.writerow( (u['username'], u['contribs'], u['email']) )
            except UnicodeEncodeError:
                writer.writerow( ("error!") )    


if __name__ == '__main__':
    p = parameters.Params()
    criteria = p.getCriteria('curation tools newcomers') #pass in as sysarg
#     print criteria
    paths = p.getPaths('curation tools newcomers')
    d = data.Download(paths['api call'], paths['file path'])
    d.downloadData()
    raw_data = d.convertJSON()
    db = data.Database('curation tools newcomers')


    sample_unix_time = raw_data['meta']['time'] #extract POSIX
    sample_datetime = datetime.utcfromtimestamp(sample_unix_time) #datetime tuple from POSIX
    user_data = raw_data['success']

    filtered_user_data = d.filterDataByDate(sample_datetime, criteria['from days ago'], criteria['to days ago'], criteria['days since edit'], user_data)
#     print filtered_user_data
    user_list = makeSample(filtered_user_data, criteria, db)
#     print user_list
    user_list = getEmails(user_list, db)
#     print len(user_list)
    print user_list

    createSampleFile(user_list, sample_datetime)

