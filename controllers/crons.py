#!/usr/bin/env python

import time
import webapp2,re
from datetime import datetime,timedelta
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import memcache
from models.models import *
import json


# The cron controllers:


class EachDayUpdate(webapp2.RequestHandler):

	# The get method is executed once per day,
	# and it creates a new Day entry from the last
	# 24 hours worth of pings.

	def get(self):

		keyword_Dictioanry={};
		location_Dictioanry={};
		stop_words={"based","company","corporation","productions","corp","year","from"};
		for i in range(1,4):
			url= "https://api.angel.co/1/jobs?page="+str(i);
			print url;
			#url= "http://localhost/phpmyadmin/www/index"+str(i)+".html";
		
			result = urlfetch.fetch(url,
						deadline=10,
						headers={'Cache-Control' : 'max-age=0'})
			if result.status_code == 200:
				data = json.loads(result.content);
				#self.response.out.write(result.content);
				for x in data['jobs']:
					keyword_TagList=[];
					location_TagList=[];
			
			
					flag = False;

					for y in x['tags']:

						if(y['tag_type']=="LocationTag"):
							for z in y['name'].split(","):
								location_TagList.append(z.lower())
							

						elif(y['tag_type']=="SkillTag"):
							
							for keysplit in re.findall(r"[\w']+", y['name']):
								if(len(keysplit)>3):
									keysplit=keysplit.lower();
							#print keysplit;
									if( list ( set ( [keysplit]) - set(stop_words) ) ):
										keyword_TagList.append(keysplit)
					
						elif(y['tag_type']=="RoleTag"):
							if(y['id']==103480 or y['id']==80489 or y['id']==80487 or y['id']==80488 or y['id']==103479 or y['id']==103477):
								flag = True;
						
							

					if flag:

						feed_data = memcache.get(str(x['id']))
						if not feed_data:
							feed_data = x
							memcache.set(str(x['id']), feed_data, time=86400)

						for keysplit in re.findall(r"[\w']+", x['startup']['name']):
							if(len(keysplit)>3):
								keysplit=keysplit.lower();
								if(list(set([keysplit])-set(stop_words))):
									keyword_TagList.append(keysplit)
						for tags in keyword_TagList:
							if(keyword_Dictioanry.has_key(tags)):
								keyword_Dictioanry.get(tags).append(x['id'])
							else:
								keyword_Dictioanry.update({tags:[x['id']]});	

						for tags in location_TagList:
							if(location_Dictioanry.has_key(tags)):
								location_Dictioanry.get(tags).append(x['id'])
							else:
								location_Dictioanry.update({tags:[x['id']]});
						

		for tags in location_Dictioanry.keys():
			location_key=LocationTags.get_by_key_name(tags)
			#location_key = db.get(key)
			if not location_key:
				location_key=LocationTags(key_name=tags, jobids=location_Dictioanry.get(tags))
			location_key.jobids=location_Dictioanry.get(tags);
			location_key.put();

		for tags in keyword_Dictioanry.keys():
			keyword_key=KeywordTags.get_by_key_name(tags)
			#keyword_key = db.get(key)
			if not keyword_key:
				keyword_key=KeywordTags(key_name=tags, jobids=keyword_Dictioanry.get(tags))
			
			keyword_key.jobids=keyword_Dictioanry.get(tags);
			keyword_key.put();

		self.response.write("Things successfully Updated to Datastore");
			
			
		
				



				


			
		