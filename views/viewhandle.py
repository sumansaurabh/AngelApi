#!/usr/bin/env python

import webapp2
import urllib2,json
import jinja2
import os
import cgi, cgitb
from models.models import *
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
		for key in keyword.split():
			key=key.lower();
			keyword_key=KeywordTags.get_by_key_name(key);
			if keyword_key:
				keyword_db.extend(keyword_key.jobids);

		for key in location.split():
			key=key.lower();
			location_key=LocationTags.get_by_key_name(key)
			if location_key:
				location_db.extend(location_key.jobids);
			
		
		if location and keyword:
			temp=list(set(location_db) & set(keyword_db));
			if temp:
				self.response.write("<p style='font-size:15px; text-align:center'>Tags Used: <b><font color='red'>"+location+"</b>, <b>"+keyword+"</font></b></p>");
				
			else:
				self.response.write("<p style='font-size:15px; text-align:center'>No Results for the Tag: <b><font color='red'>"+location+"</b>, <b>"+keyword+"</font></b></p>");

			for x in temp:
				try:
					self.printData(x)
				except Exception, e:
					continue;

		if keyword:
			temp=list(set(keyword_db));
			if temp:	
				self.response.write("<p style='font-size:15px; text-align:center'>Tags Used: <b><font color='red'>"+keyword+"</font></b></p>");
			else:
				self.response.write("<p style='font-size:15px; text-align:center'>No Results for the Tag: <b><font color='red'>"+keyword+"</font></b></p>");
			for x in temp:
				try:
					self.printData(x);
				except Exception, e:
					continue;
		if location:
			temp=list(set(location_db));
			if temp:

				self.response.write("<p style='font-size:15px; text-align:center' >Tags Used: <b><font color='red'>"+location+"</font></b></p>");
			else:
				self.response.write("<p style='font-size:15px; text-align:center' >No Results for the Tag: <b><font color='red'>"+location+"</font></b></p>");
			for x in temp:
				
				try:
					self.printData(x);
				except Exception, e:
					continue;
				
			
		
		
		
		#response = urllib2.urlopen("https://api.angel.co/1/jobs?page=1");
		
		
		
		return;

	def printData(self,x):
		feed_data = memcache.get(str(x))
		if not feed_data:
			self.response.write("Given search index not present, memcache needs to updated");
			return;


		self.response.write(" <table style='width:1400px'>");

		self.response.write("<tr>");

		
		self.response.write("<th scope='row'><a href="+feed_data['angellist_url']+"><img src='"+feed_data['startup']['thumb_url']+"' ></a>	</th>");
		self.response.write("<td>");

		self.response.write(" <table style='width:900px'>");

		self.response.write("<tr>");
		self.response.write("<td>");

		try :
			feed_data['startup']['high_concept'].decode('ascii','ignore');
			#feed_data['startup']['high_concept.replace("\u","*");
			#.replace("\u", "*".replace('0x','*'));

		except Exception, e:
			feed_data['startup']['high_concept']="None"

		try:
			feed_data['title'].decode('utf-8','ignore');
			#.replace("\u", "*").replace('0x','*'));
		except Exception, e:
			feed_data['title']="None"
			
		self.response.write("<h2><a href="+feed_data['startup']['company_url']+">"+feed_data['startup']['name']+"</a> <h3>"+feed_data['startup']['high_concept']+"</h3></h2>");
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
		self.response.write("<td>"+str(feed_data['equity_cliff'])+"</td>");
		self.response.write("<td>"+str(feed_data['equity_min'])+" - "+str(feed_data['equity_max'])+"</td>");
		self.response.write("<td>"+str(feed_data['equity_vest'])+"</td>");
		self.response.write("<td>"+str(feed_data['startup']['follower_count'])+"</td>");
		self.response.write("</table>");
		self.response.write("</td>");
		self.response.write("</tr>");
		self.response.write("</table>");	
		self.response.write("</td>");
		self.response.write("</tr>");

		self.response.write("<tr>");
		self.response.write("<th scope='row'>Job Type</th>");
		self.response.write("<td>"+feed_data['title']+" ("+feed_data['job_type']+")</td>");
		self.response.write("</tr>");
		
		self.response.write("<tr>");
		self.response.write("<th scope='row'>Salary</th>");
		self.response.write("<td>"+str(feed_data['salary_min'])+" - "+str(feed_data['salary_max'])+"</td>");
		self.response.write("</tr>");
		for tags in feed_data['tags']:
			if tags['tag_type']=="LocationTag":
				self.response.write("<tr>");
				self.response.write("<th scope='row'>Location</th>");
				self.response.write("<td>"+tags['display_name']+"</td>");
				self.response.write("</tr>");
		
		self.response.write("<tr>");
		self.response.write("<th scope='row'>StartUp Description</th>");
		self.response.write("<td>");
		var=feed_data['startup']['product_desc'];

		
		try:
			self.response.write(var.decode('utf-8','ignore').encode("utf-8",'ignore'));
			#.replace("\u", "*").replace('0x','*'));
		except Exception, e:
			self.response.write("None");
		self.response.write("</td>");
		self.response.write("</tr>");
		self.response.write("</table>");

		self.response.write("<hr>");

		#self.response.write(feed_data)


