#!/usr/bin/env python


import webapp2,re
from datetime import datetime
from google.appengine.api import urlfetch
from google.appengine.ext import db
from google.appengine.api import memcache
from models.models import *
import json


# The cron controllers:


class UpdateDatastore(webapp2.RequestHandler):

	# The get method is executed once per day,
	# and it creates a new Day entry from the last
	# 24 hours worth of pings.

	def get(self):

		a = datetime.now()
		#db.delete(KeywordTags.all(keys_only=True))
		#db.delete(LocationTags.all(keys_only=True))
		self.keyword_Dictioanry={};
		self.location_Dictioanry={};
		
		rpcs=[];
		
		for i in range(1,10):
			url= "https://api.angel.co/1/jobs?page="+str(i);
			print url;
			#url= "http://localhost/phpmyadmin/www/index"+str(i)+".html";
			
			rpc = urlfetch.create_rpc(deadline=10)
			urlfetch.make_fetch_call(rpc, url)
			rpc.callback = self.create_callback(rpc)
			#rpc.wait()
			rpcs.append(rpc)
			

		# Finish all RPCs, and let callbacks process the results.
		for rpc in rpcs:
			rpc.wait();

		for tags in self.location_Dictioanry.keys():
			location_key=LocationTags.get_by_key_name(tags)
			#location_key = db.get(key)
			if not location_key:
				location_key=LocationTags(key_name=tags, jobids=self.location_Dictioanry.get(tags))
			location_key.jobids=self.location_Dictioanry.get(tags);
			location_key.put();

		for tags in self.keyword_Dictioanry.keys():
			keyword_key=KeywordTags.get_by_key_name(tags)
			#keyword_key = db.get(key)
			if not keyword_key:
				keyword_key=KeywordTags(key_name=tags, jobids=self.keyword_Dictioanry.get(tags))
			
			keyword_key.jobids=self.keyword_Dictioanry.get(tags);
			keyword_key.put();

		b = datetime.now()
		self.response.write("Time taken for Update: "+str(b-a));
		self.response.write("Things successfully Updated to Datastore");
		return;

	def create_callback(self,rpc):
		return lambda: self.handle_result(rpc)

	def handle_result(self,rpc):
		stop_words={"based","company","corporation","productions","corp","year","from"};
		result = rpc.get_result()
		data = json.loads(result.content);
		
		if not data:
			return

    	
				#self.response.out.write(result.content);
		for x in data['jobs']:
			keyword_TagList=[];
			location_TagList=[];
			
			location_str="";
			flag = False;

			for y in x['tags']:

				if(y['tag_type']=="LocationTag"):
					location_str=y['display_name'];
					for z in re.findall(r"[\w']+", y['name']):
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
					self._getMemCache(feed_data,location_str)
					
				if not x['startup']['hidden']:
					for keysplit in re.findall(r"[\w']+", x['startup']['name']):
						if(len(keysplit)>3):
							keysplit=keysplit.lower();
							if(list(set([keysplit])-set(stop_words))):
								keyword_TagList.append(keysplit)
				for tags in keyword_TagList:
					if(self.keyword_Dictioanry.has_key(tags)):
						self.keyword_Dictioanry.get(tags).append(x['id'])
					else:
						self.keyword_Dictioanry.update({tags:[x['id']]});	
				for tags in location_TagList:
					if(self.location_Dictioanry.has_key(tags)):
						self.location_Dictioanry.get(tags).append(x['id'])
					else:
						self.location_Dictioanry.update({tags:[x['id']]});
						

		
		


	def _getMemCache(self,feed_data,location_str):
		feed_dictionary={};

		
		feed_dictionary.update({"title": feed_data['title']})
		feed_dictionary.update({"equity_cliff": feed_data['equity_cliff']})
		feed_dictionary.update({"equity_min": feed_data['equity_min']})
		feed_dictionary.update({"equity_max": feed_data['equity_max']})
		feed_dictionary.update({"equity_vest": feed_data['equity_vest']})
		feed_dictionary.update({"salary_min": feed_data['salary_min']})
		feed_dictionary.update({"salary_max": feed_data['salary_max']})
		feed_dictionary.update({"job_type": feed_data['job_type']})
		feed_dictionary.update({"angellist_url": feed_data['angellist_url']})
		feed_dictionary.update({"location": location_str})
		#feed_dictionary.update({"startup_hidden": feed_data['startup']['hidden']})
		#feed_data['startup']['hidden']=feed_data['startup']['hidden'].lower();
		if not feed_data['startup']['hidden']:
			feed_dictionary.update({"startup_name": feed_data['startup']['name']})
			feed_dictionary.update({"startup_thumb_url": feed_data['startup']['thumb_url']})
			feed_dictionary.update({"startup_product_desc": feed_data['startup']['product_desc']})
			feed_dictionary.update({"startup_high_concept": feed_data['startup']['high_concept']})
			feed_dictionary.update({"startup_follower_count": feed_data['startup']['follower_count']})
			feed_dictionary.update({"startup_company_url": feed_data['startup']['company_url']})

		memcache.set(str(feed_data['id']), feed_dictionary, time=864000)
		

			
			
		
				



				


			
		