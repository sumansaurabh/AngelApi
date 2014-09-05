#!/usr/bin/python

import json, urllib

# Import modules for CGI handling 
import cgi, cgitb
#from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from google.appengine.api import users
import webapp2

import Load_JobProfile
import thread
import time

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 


response="""<html>
		<head>
 		<style type="text/css">

    html, body, div, span, object, iframe,
     blockquote, pre,
    abbr, address, cite, code,
    del, dfn, em, img, ins, kbd, q, samp,
    small, strong, sub, sup, var,
    b, i,
    dl, dt, dd, ol, ul, li,
    fieldset, form, label, legend,
    table, caption, tbody, tfoot, thead, tr, th, td {
        margin:0;
        padding:0;
        border:0;
        outline:0;
        font-size:100%;
        vertical-align:baseline;
        background:transparent;
    }
    

    body {
        margin:0;
        padding:0;
        font:18px/20px "Helvetica Neue",Arial, Helvetica, sans-serif;
        color: #555;
        background:#f5f5f5 url(bg.jpg);
    }
    
    a {color:#666;}
    
    #content {width:65%; max-width:690px; margin:6% auto 0;}
    
    /*
    Pretty Table Styling
    CSS Tricks also has a nice writeup: http://css-tricks.com/feature-table-design/
    */
    
    table {
        overflow:hidden;
        border:0px solid #d3d3d3;
        background:#fefefe;
        width:70%;
        margin:1% auto 0;
        -moz-border-radius:5px; /* FF1+ */
        -webkit-border-radius:5px; /* Saf3-4 */
        border-radius:5px;
        -moz-box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
        -webkit-box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
    }
    
    th, td {padding:0px 28px 18px; text-align:left; }

    
    
    td,th {padding-top:12px; text-shadow: 1px 1px 1px #fff; background:#e8eaeb;}
    
    td {border-top:1px solid #e0e0e0; border-right:1px solid #e0e0e0;}
    
    tr.odd-row td {background:#f6f6f6;}
    
    td.first, th.first {text-align:left}
    
    td.last {border-right:none;}
    
    /*
    Background gradients are completely unnecessary but a neat effect.
    */
    
    td {
        background: -moz-linear-gradient(100% 25% 90deg, #fefefe, #f9f9f9);
        background: -webkit-gradient(linear, 0% 0%, 0% 25%, from(#f9f9f9), to(#fefefe));
    }
    
    tr.odd-row td {
        background: -moz-linear-gradient(100% 25% 90deg, #f6f6f6, #f1f1f1);
        background: -webkit-gradient(linear, 0% 0%, 0% 25%, from(#f1f1f1), to(#f6f6f6));
    }
    
    th {
        background: -moz-linear-gradient(100% 20% 90deg, #e8eaeb, #ededed);
        background: -webkit-gradient(linear, 0% 0%, 0% 20%, from(#ededed), to(#e8eaeb));
    }
    
    
    tr:first-child th.first {
        -moz-border-radius-topleft:5px;
        -webkit-border-top-left-radius:5px; /* Saf3-4 */
    }
    
    tr:first-child th.last {
        -moz-border-radius-topright:5px;
        -webkit-border-top-right-radius:5px; /* Saf3-4 */
    }
    
    tr:last-child td.first {
        -moz-border-radius-bottomleft:5px;
        -webkit-border-bottom-left-radius:5px; /* Saf3-4 */
    }
    
    tr:last-child td.last {
        -moz-border-radius-bottomright:5px;
        -webkit-border-bottom-right-radius:5px; /* Saf3-4 */
    	}
    #default{
    	width:99%;
    	margin:1% auto 0;
    }
    #default td, #default th {
    	font-size: 1em;
    	border: 0px ;
    	padding: 3px 7px 2px 7px;
    	background:white;
	}
	width:70%;

</style>
<title>Find Your Jobs</title>
</head>
<body>

<h1 font size="24" align="center">Find Your Jobs</h1>
	<form enctype="multipart/form-data" method="post">
		<table id ="default"> 
			<tr  >
				<th></th>
				<th style="text-align:left; font-size:22px">Keyword</th>
				<th style="text-align:left; font-size:22px">Location / Place</th>
				
				<th></th>
				<th></th>
				

			</tr>
			<tr>
				<td></td>
				<td style="text-align:left; font-size:22px"><input type="text" name="keyword"></td>
				<td style="text-align:left; font-size:22px"><input type="text" name="location"></td>
				<td style="text-align:left; font-size:22px"><input type="submit" value="Submit"><td>
				
				<td></td>
				
				
			</tr>

		<table> 
	</form>

	"""
class MainPage(webapp2.RequestHandler):
	
	#Handler for the GET requests
	
	def get(self):
		#self.response.headers['Content-Type'] = 'text/plain'
		if(not schedule_Database.dataLoaded):
			self.response.write("Opps!!! Server Busy");
		else:
			self.response.write(response)
		

		
	

	#Handler for the POST requests
	def post(self):
		if(not schedule_Database.dataLoaded):
			self.response.write("Opps!!! Server Busy");
		else:
			
		#print "##### ",self.request.get('keyword')
			keyword = self.request.get('keyword')
			location = self.request.get('location')
			#Load_JobProfile.keyWord_Searching(cgi.escape(self.request.get('keyword')));
			#Load_JobProfile.finds_Jobs_Data(cgi.escape(self.request.get('location')))
			Load_JobProfile.keyWord_Searching(keyword);
			Load_JobProfile.finds_Jobs_Data(keyword,location)

			self.response.write(response)
			self.respond_POST(keyword,location)
			self.response.write('</body>\n</html>')
		
		
		return			

	def respond_POST(self,keyword,location,status=200):

		

		if(location and keyword):
			if (len(Load_JobProfile.jobs_db)):
				self.response.write("<p style='font-size:15px; text-align:center'>Tags Used: <b><font color='red'>"+location+"</b>, <b>"+keyword+"</font></b></p>");
			else:
				self.response.write("<p style='font-size:15px; text-align:left'>No Results for the Tag: <b><font color='red'>"+location+"</b>, <b>"+keyword+"</font></b></p>");
		
			for x in list(set(Load_JobProfile.jobs_db)):
				try:
					self.display_jobs(Load_JobProfile.ag.JOBS_DICTIONARY[x]);
				except Exception, e:
					continue;
			
		#print ag.JOBS_DICTIONARY[x];
		if keyword:
			
			if (len(Load_JobProfile.jobs_db_skill)):	
				self.response.write("<p style='font-size:15px; text-align:center'>Tags Used: <b><font color='red'>"+keyword+"</font></b></p>");
			else:
				self.response.write("<p style='font-size:15px; text-align:left'>No Results for the Tag: <b><font color='red'>"+keyword+"</font></b></p>");
			for x in list(set(Load_JobProfile.jobs_db_skill)):
				try:
					self.display_jobs(Load_JobProfile.ag.JOBS_DICTIONARY[x]);
				except Exception, e:
					continue;
		if location:
			if (len(Load_JobProfile.jobs_db_loc)):

				self.response.write("<p style='font-size:15px; text-align:center' >Tags Used: <b><font color='red'>"+location+"</font></b></p>");
			else:
				self.response.write("<p style='font-size:15px; text-align:left' >No Results for the Tag: <b><font color='red'>"+location+"</font></b></p>");
			for x in list(set(Load_JobProfile.jobs_db_loc)):
				try:
					self.display_jobs(Load_JobProfile.ag.JOBS_DICTIONARY[x]);
				except Exception, e:
					continue;

		Load_JobProfile.clean_JobsMemory();
		

	def display_jobs(self,jobsDescription):
	
		#self.response.write("<h2> Job Details </h2>");
		self.response.write(" <table style='width:1400px'>");

		self.response.write("<tr>");

		
		self.response.write("<th scope='row'><a href="+jobsDescription.angellist_url+"><img src='"+jobsDescription.startup_thumb_url+"' ></a>	</th>");
		self.response.write("<td>");

		self.response.write(" <table style='width:900px'>");

		self.response.write("<tr>");
		self.response.write("<td>");

		try :
			jobsDescription.startup_high_concept.decode('ascii','ignore');
			#jobsDescription.startup_high_concept.replace("\u","*");
			#.replace("\u", "*").replace('0x','*'));

		except Exception, e:
			jobsDescription.startup_high_concept="None"

		if jobsDescription.title :
			jobsDescription.title.decode('utf-8','ignore');
			#.replace("\u", "*").replace('0x','*'));
		else :
			jobsDescription.title="None"
			
		self.response.write("<h2><a href="+jobsDescription.startup_company_url+">"+jobsDescription.startup_name+"</a> <h3>"+jobsDescription.startup_high_concept+"</h3></h2>");
		self.response.write("</td>");
		self.response.write("</tr>");

		self.response.write("<tr>");
		self.response.write("<td>");
		self.response.write(" <table style='width:1200px'>");
		self.response.write("<th >Equity Cliff</th>");
		self.response.write("<th >Equity</th>");
		self.response.write("<th>Equity Vest</th>");
		self.response.write("<th>StartUp Follower</th>");
		self.response.write("</tr>")
		self.response.write("<tr>")
		self.response.write("<td>"+str(jobsDescription.equity_cliff)+"</td>");
		self.response.write("<td>"+str(jobsDescription.equity_min)+" - "+str(jobsDescription.equity_max)+"</td>");
		self.response.write("<td>"+str(jobsDescription.equity_vest)+"</td>");
		self.response.write("<td>"+str(jobsDescription.startup_follower_count)+"</td>");
		self.response.write("</table>")
		self.response.write("</td>")
		self.response.write("</tr>")
		self.response.write("</table>")	
		self.response.write("</td>");
		self.response.write("</tr>");

		self.response.write("<tr>");
		self.response.write("<th scope='row'>Job Type</th>");
		self.response.write("<td>"+jobsDescription.title+" ("+jobsDescription.job_type+")</td>");
		self.response.write("</tr>");
		
		self.response.write("<tr>");
		self.response.write("<th scope='row'>Salary</th>");
		self.response.write("<td>"+str(jobsDescription.salary_min)+" - "+str(jobsDescription.salary_max)+"</td>");
		self.response.write("</tr>");
		
		self.response.write("<tr>");
		self.response.write("<th scope='row'>Location</th>");
		self.response.write("<td>"+jobsDescription.location+"</td>");
		self.response.write("</tr>");
	
		self.response.write("<tr>")
		self.response.write("<th scope='row'>StartUp Description</th>");
		self.response.write("<td>")
		var=jobsDescription.startup_product_desc;

		if var :
			self.response.write(var.decode('utf-8','ignore').encode("utf-8",'ignore'));
			#.replace("\u", "*").replace('0x','*'));
		else :
			self.response.write("None");
		self.response.write("</td>");
		self.response.write("</tr>");
		self.response.write("</table>")

		self.response.write("<hr>")
	
def schedule_Database( threadName, delay ):
	while True:
		schedule_Database.dataLoaded=False;
		print "Loading Database...........";
		Load_JobProfile.Load_Data();
		print "Database Loaded";
		schedule_Database.dataLoaded=True;
		time.sleep(86400)





try:
	thread.start_new_thread( schedule_Database, ("Thread-1", 2, ) )
except Exception, e:
	print "Error: unable to start thread"
	
	
	
application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
	