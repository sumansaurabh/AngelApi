#!/usr/bin/python
import json, urllib,re

# Import modules for CGI handling 
import cgi, cgitb
from AngelApi import *


# Create instance of FieldStorage
ag=AngelApi();
jobs_db=[];
jobs_db_loc=[];
jobs_db_skill=[];
keyword_db=[];

#This method should be run once a day
def Load_Data():
	ag.Load_KeyWordTag();
	ag.Load_LocationTag();
	ag.Update_Jobs();

def clean_JobsMemory():
	while len(jobs_db) > 0 : jobs_db.pop()
	while len(jobs_db_loc) > 0 : jobs_db_loc.pop()
	while len(jobs_db_skill) > 0 : jobs_db_skill.pop()
	while len(jobs_db_skill) > 0 : keyword_db.pop();

def finds_Jobs_Data(keyword,location):
	
	if location:
		
		for x in ag.LOCATION_TAGS.keys():
			
			split_location=map(str.lower,x.replace(',','').split());
			
			if(set(split_location) & set(location.split())):
				
				location_jobs=ag.LOCATION_TAGS.get(x.lower());
				
				for key in keyword_db:
					skill_jobs=ag.KeyWord_Tag.get(key);
					for x in list(set(location_jobs) & set(skill_jobs)):
						jobs_db.append(x);
				
				jobs_db_loc.extend(list(set(location_jobs) - set(jobs_db)));

		
	for key in keyword_db:
		skill_jobs=ag.KeyWord_Tag.get(key);
		jobs_db_skill.extend(list(set(skill_jobs) - set(jobs_db)));
		#print "@@@@",key,"--",

	#print "Jobs List",list(set(jobs_db));
	#print "Jobs List",list(set(jobs_db_loc));
	#print "Jobs List",list(set(jobs_db_skill));

def keyWord_Searching(keyword):

	if(not keyword):
		return;
	while len(keyword_db) > 0 : keyword_db.pop()
	stop_words={"based","company","corporation","productions","corp","year","from"};
	

	keyword_prune=[];
	for keysplit in re.findall(r"[\w']+", keyword):
		if(len(keysplit)>3):
			keysplit=keysplit.lower();
			if( list ( set ( [keysplit]) - set(stop_words) ) ):
				keyword_prune.append(keysplit);
	#split_keyword=map(str.lower,keyword.split());
	#keyword_prune.extend( list ( set ( split_keyword) - set(stop_words) ) );

	#print "#########",keyword_prune
	
	for x in ag.KeyWord_Tag.keys():
		split_keyword=map(str.lower,x.split());
		if(set(split_keyword) & set(keyword_prune)):
			keyword_db.append(x);			
	

	
		






			







"""	

keyword="";
location="new york, ny";

if(keyword or location):
	Load_Data();
	keyWord_Searching(keyword);
	finds_Jobs_Data(keyword,location="");

	#print "##########\n",jobs_db;
	#print "##########\n",ag.LOCATION_TAGS;
	#print "##########\n",jobs_db_skill;
	#print "##########\n",keyword_db;

	for x in ag.LOCATION_TAGS.keys():
		print x,"--",ag.LOCATION_TAGS[x];


	if (len(jobs_db)):
		print "<p style='font-size:12px; text-align:center'>Tags Used: <b>Location</b> and <b>Keywords</b></p>"
	for x in list(set(jobs_db)):
		display_jobs(ag.JOBS_DICTIONARY[x]);
		#print ag.JOBS_DICTIONARY[x];

	if (len(jobs_db_skill)):	
		print "<p style='font-size:12px; text-align:center'>Tags Used: <b>Keyword</b></p>"
	for x in list(set(jobs_db_skill)):
		display_jobs(ag.JOBS_DICTIONARY[x]);
	
	
	if (len(jobs_db_loc)):
		print "<p style='font-size:12px; text-align:center' >Tags Used: <b>Location</b></p>"
	for x in list(set(jobs_db_loc)):

		display_jobs(ag.JOBS_DICTIONARY[x]);
		#print ag.JOBS_DICTIONARY[x];
		


print "</body>"
print "</html>"

"""