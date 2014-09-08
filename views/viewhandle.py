#!/usr/bin/env python

import webapp2
import urllib2,json
import jinja2
import os,re
import cgi, cgitb
from models.models import *
from google.appengine.api import urlfetch
from google.appengine.api import memcache

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



class MainHandler(webapp2.RequestHandler):
	"""This is the view class, gets the post request and dispalys the jobs """

	def post(self):
		
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))


		keyword_db=[];
		location_db=[];
		
		
		keyword = self.request.get('keyword');
		location = self.request.get('location');
		#keyword="sales"
		#location="gurgaon"
		
		"""Retriving request form database"""
		for key in re.findall(r"[\w']+",keyword):
			key=key.lower();
			keyword_key=KeywordTags.get_by_key_name(key);
			if keyword_key:
				keyword_db.extend(keyword_key.jobids);

		for key in re.findall(r"[\w']+", location):
			key=key.lower();
			location_key=LocationTags.get_by_key_name(key)
			if location_key:
				location_db.extend(location_key.jobids);
			
		temp=[];
		if location and keyword:
			temp=list(set(location_db) & set(keyword_db));
			if temp:
				self.response.write("<p style='font-size:15px; text-align:center'>Tags Used: <b><font color='red'>"+location+"</b>, <b>"+keyword+"</font></b></p>");
			else:
				self.response.write("<p style='font-size:15px; text-align:center'>No Results for the Tag: <b><font color='red'>"+location+"</b>, <b>"+keyword+"</font></b></p>");

			

		elif keyword:
			temp=list(set(keyword_db));
			if temp:	
				self.response.write("<p style='font-size:15px; text-align:center'>Tags Used: <b><font color='red'>"+keyword+"</font></b></p>");
			else:
				self.response.write("<p style='font-size:15px; text-align:center'>No Results for the Tag: <b><font color='red'>"+keyword+"</font></b></p>");
			
		else:
			temp=list(set(location_db));
			if temp:
				self.response.write("<p style='font-size:15px; text-align:center' >Tags Used: <b><font color='red'>"+location+"</font></b></p>");
			else:
				self.response.write("<p style='font-size:15px; text-align:center' >No Results for the Tag: <b><font color='red'>"+location+"</font></b></p>");
		
		rpcs=[];
		i=1;
		for x in temp:
			
			feed_data = memcache.get(str(x))
				#If not present in memecache load the result back in memcahce
			if feed_data:
				
				#self.response.write(feed_data)
				self.printData(feed_data)
			else:
				#self.response.write("load memcache")
					##Loads max of 10 job in memory
				if i==5:
					continue;
				i+=1
				url="https://api.angel.co/1/jobs/"+str(x)
				rpc = urlfetch.create_rpc(deadline=10)
				urlfetch.make_fetch_call(rpc, url)
				rpc.callback = self.create_callback(rpc)
				rpcs.append(rpc)
			
		for rpc in rpcs:
			rpc.wait();

	def create_callback(self,rpc):
		return lambda: self.handle_result(rpc)

	def handle_result(self,rpc):
		result = rpc.get_result()
		feed_data = json.loads(result.content);

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

		for tags in feed_data.get('tags'):
			if tags['tag_type']=="LocationTag":
				feed_dictionary.update({"location": tags['display_name']})

		feed_dictionary.update({"startup_hidden": feed_data['startup']['hidden']})

		if not feed_data['startup']['hidden']:
			feed_dictionary.update({"startup_name": feed_data['startup']['name']})
			feed_dictionary.update({"startup_thumb_url": feed_data['startup']['thumb_url']})
			feed_dictionary.update({"startup_product_desc": feed_data['startup']['product_desc']})
			feed_dictionary.update({"startup_high_concept": feed_data['startup']['high_concept']})
			feed_dictionary.update({"startup_follower_count": feed_data['startup']['follower_count']})
			feed_dictionary.update({"startup_company_url": feed_data['startup']['company_url']})

		memcache.set(str(feed_data['id']), feed_dictionary, time=864000)
		
		self.printData(feed_dictionary)	
		return;

	def printData(self,feed_data):
		self.response.write(" <table style='width:1400px'>");

		self.response.write("<tr>");

		
		self.response.write("<th scope='row'><a href="+str(feed_data.get('angellist_url'))+"><img src='"+str(feed_data.get('startup_thumb_url'))+"' ></a>	</th>");
		self.response.write("<td>");

		self.response.write(" <table style='width:900px'>");

		self.response.write("<tr>");
		self.response.write("<td>");

		try :
			feed_data.get('startup_high_concept').decode('ascii','ignore');
			#feed_data.get('startup')['high_concept.replace("\u","*");
			#.replace("\u", "*".replace('0x','*'));

		except Exception, e:
			feed_data.update({"startup_high_concept":"Not Available"});

		try:
			feed_data.get('title').decode('utf-8','ignore');
			#.replace("\u", "*").replace('0x','*'));
		except Exception, e:
			feed_data.update({"title":"Not Available"});
			
		self.response.write("<h2><a href="+str(feed_data.get('startup_company_url'))+">"+str(feed_data.get('startup_name'))+"</a> <h3>"+str(feed_data.get('startup_high_concept'))+"</h3></h2>");
		self.response.write("</td>");
		self.response.write("</tr>");

		self.response.write("<tr>");
		self.response.write("<td>");
		self.response.write(" <table style='width:1200px'>");
		self.response.write("<th >Equity Cliff</th>");
		self.response.write("<th >Equity</th>");
		self.response.write("<th>Equity Vest</th>");
		self.response.write("<th>StartUp Follower</th>");
		self.response.write("</tr>");
		self.response.write("<tr>");
		self.response.write("<td>"+str(feed_data.get('equity_cliff'))+"</td>");
		self.response.write("<td>"+str(feed_data.get('equity_min'))+" - "+str(feed_data.get('equity_max'))+"</td>");
		self.response.write("<td>"+str(feed_data.get('equity_vest'))+"</td>");
		self.response.write("<td>"+str(feed_data.get('startup_follower_count'))+"</td>");
		self.response.write("</table>");
		self.response.write("</td>");
		self.response.write("</tr>");
		self.response.write("</table>");	
		self.response.write("</td>");
		self.response.write("</tr>");

		self.response.write("<tr>");
		self.response.write("<th scope='row'>Job Type</th>");
		self.response.write("<td>"+str(feed_data.get('title'))+" ("+str(feed_data.get('job_type'))+")</td>");
		self.response.write("</tr>");
		
		self.response.write("<tr>");
		self.response.write("<th scope='row'>Salary</th>");
		self.response.write("<td>"+str(feed_data.get('salary_min'))+" - "+str(feed_data.get('salary_max'))+"</td>");
		self.response.write("</tr>");

		self.response.write("<tr>");
		self.response.write("<th scope='row'>Location</th>");
		self.response.write("<td>"+str(feed_data.get('location'))+"</td>");
		self.response.write("</tr>");

		
		
		self.response.write("<tr>");
		self.response.write("<th scope='row'>StartUp Description</th>");
		self.response.write("<td>");
		var=feed_data.get('startup_product_desc');

		
		try:
			self.response.write(var.decode('utf-8','ignore').encode("utf-8",'ignore'));
			#.replace("\u", "*").replace('0x','*'));
		except Exception, e:
			self.response.write("Not Available");
		self.response.write("</td>");
		self.response.write("</tr>");
		self.response.write("</table>");

		self.response.write("<hr>");

		#self.response.write(feed_data)



