#!/usr/bin/python
import urllib,json
from Jobs import *
class AngelApi:

	LOCATION_TAGS={};
	ROLE_TAGS={};
	KeyWord_Tag={};
	JOBS_DICTIONARY={};
	def Load_KeyWordTag(self):
		#print "----- loading Skill Tag------";
		with open("Tag_Ids/Keywords_Tag") as f:
			for line in f:  #Line is a string
				string = line.split();
				jobs=[];
				for x in range(2,len(string)):
					string[1]+=" "+string[x];
				tags={string[1] : jobs};
				AngelApi.KeyWord_Tag.update(tags);
			#_TAGS={_str[0] : _str[1]};
			#KeyWord_Tag_ID.update(_TAGS);
		#print "----- Successfully Loaded Skill Tag------";
		return;

	def Load_LocationTag(self):
		#print "----- loading Location Tag------";
		with open("Tag_Ids/Location_Tag") as f:
			for line in f:  #Line is a string
				string = line.split();
				jobs=[];
				for x in range(2,len(string)):
					string[1]+=" "+string[x];
				tags={string[1] : jobs};
				AngelApi.LOCATION_TAGS.update(tags);
		#print "----- Successfully Loaded Location Tag------";
		return;

	def Update_Jobs(self):
		#print "----- Updating Job Details------";
		count = 1;
		for i in range(1,11):
			url= "https://api.angel.co/1/jobs?page="+str(i);
			print url;
			#url= "http://localhost/phpmyadmin/www/index"+str(i)+".html";
			response = urllib.urlopen(url);
			
			#try:
			data = json.loads(response.read());
			
			for x in data['jobs']:
				
				jobs = Jobs();
				AngelApi._Profile_Jobs(self,x,jobs);
				jobs_dict = { count : jobs};
				skill_tag_name=[];
				for y in x['tags']:
					if(y['tag_type']=="SkillTag"):
						skill_tag_name.append(y['name']);
					elif(y['tag_type']=="LocationTag"):
						loc_tag_name=y['name'];
					elif(y['tag_type']=="RoleTag"):
						if(y['id']==103480 or y['id']==80489 or y['id']==80487 or y['id']==80488 or y['id']==103479 or y['id']==103477):
							#print "Job No : ",count," Location = ",loc_tag_name;

							AngelApi.JOBS_DICTIONARY.update(jobs_dict);

							if(loc_tag_name):
								if(AngelApi.LOCATION_TAGS.has_key(loc_tag_name)):
									AngelApi.LOCATION_TAGS.get(loc_tag_name).append(count);

							
							startup_key=""
							try:
								startup_key=x['startup']['name'];	
								if(startup_key):
									startup_key=x['startup']['name'];
									startup_key.encode('utf-8','ignore')
									if(AngelApi.KeyWord_Tag.has_key(startup_key)):
										#print "Job No : ",count," startup = ",startup_key;
										AngelApi.KeyWord_Tag.get(startup_key).append(count);# For appending company name keywords

							except Exception, e:
								print "Exception in startup name, nothing to be done: ",startup_key,
								

							for loc in skill_tag_name:
								#print "Job No : ",count," Skills = ",loc;
								if(AngelApi.KeyWord_Tag.has_key(loc)):
									if(loc):
										AngelApi.KeyWord_Tag.get(loc).append(count);
							count+=1;
						#fo.write(y['name']);
			#except (ValueError, KeyError, TypeError):
			#	print "JSON format error";
		return;

	def _Profile_Jobs(self,x,jobs):
		

		jobs.title= x['title'];
		jobs.created_at=x['created_at'];
		jobs.updated_at=x['updated_at'];
		jobs.equity_cliff=x['equity_cliff'];
		jobs.equity_min=x['equity_min'];
		jobs.equity_max=x['equity_max'];
		jobs.equity_vest=x['equity_vest'];
		jobs.salary_min=x['salary_min'];
		jobs.salary_max=x['salary_max'];
		jobs.job_type=x['job_type'];
		jobs.angellist_url=x['angellist_url'];
		jobs.startup_id=x['startup']['id'];
		if(x['startup']['hidden']):
			return;
		#print "@@@",x['startup']['hidden'];
		#print "#########3",x['startup']['name']
		
		jobs.startup_name=x['startup']['name'];
		jobs.startup_angellist_url=x['startup']['angellist_url'];
		jobs.startup_logo_url=x['startup']['logo_url'];
		jobs.startup_thumb_url=x['startup']['thumb_url'];
		#jobs.startup_product_desc=x['startup']['product_desc'].decode('utf-8',errors='ignore');

		if(x['startup']['product_desc']):
			jobs.startup_product_desc=x['startup']['product_desc'].encode('utf-8','ignore');
		
		jobs.startup_high_concept=x['startup']['high_concept'];
		jobs.startup_follower_count=x['startup']['follower_count'];
		jobs.startup_company_url=x['startup']['company_url'];

		for y in x['tags']:
			if(y['tag_type']=="LocationTag"):
				jobs.location=y['name'];

		return;


"""		
ag=AngelApi();
ag.Load_KeyWordTag();
ag.Load_LocationTag();
ag.Update_Jobs();
#print ag.LOCATION_TAGS;
#print "Give me keys",ag.JOBS_DICTIONARY.keys();
for x in ag.KeyWord_Tag.keys():
	print x," ",ag.KeyWord_Tag[x];
	"""