[AngelList Api](http://angel.co/)

#### Work Flow
	1) chmod +x * //Gives permisson to all the file
	2) Run in Terminal ./server.py
	3) Open browser - localhost:8080
	4) Keyword (Skills / Company Name ) and Location: Enter the details
5) Database shows the jobs
	a. Keyword and Location -- At the top
	b. Only Keyword 	-- At middle
	c. Only Location 	-- At bottom

#### Process
1) Keyword file contains all the keyword tag ( Skill / Comapny name ) used in angel list. This can be updated once a month.
2) Contanins Location tag. This can also be updated once a month. 

	
	##### Note
		These keyword and location tag is located in /Tag_Ids/ and can be upadated to MySQL database

3) When Server starts keyword ans location tag is loaded in memory.

########################  Part 1 (Because Job list cannot be stored in database).  
4) Sever uses [api-link](https://api.angel.co/1/jobs?page=1) to load jobs database in memory and correspondingly  This is updated once in 24 hours. 
5) Jobs are profiled as 1,2,3,4,5....... not as 'AngelList ids'.
6) A dictionary is mantained for location - jobs and keyword - jobs
	eg.
		<Boston : [4,5,9]> - Location
		<sales : [6,7,5] > - Keyword

		a) Page shows Intersection of two set is the Result [5]
		b) Only using location tag [4,9]
		c) Only using Keyword tag 	[6,7]
	#### Note
		This process undergoes faster retrival but can only be implemeted on Python based web server or the server presnt in source code .

######################	Part 2 (Each job is retrieved from database) 

7) In this case a dictioanry is maaintained for location- jobs and keyword - jobs 
	### Note
		Here Jobs are now profiled with their AngelList ids eg. 1223,1453..... and are stored in database. Every 24hrs database updated for job ids.
		eg.
			<Boston : [1123,1453, 5272]> Location
			<sales : [11453, 5476, 1123] > Keyword

		a) Page shows Intersection of two set is the Result [1123]. eg. https://api.angel.co/1/tags/1123/jobs
		b) Only using location tag [1453, 5272] 
		c) Only using Keyword tag 	[11453, 5476]

		Threads are used to retrieve each job profile.

		###Note
			This is much slower process but works on any server that supports cgi scripting.
			

Part 1 is implemented in the source code.


[ ![Codeship Status for sumansaurabh/AngelAPi](https://codeship.io/projects/88dcf450-144d-0132-971c-06b7d0e0f00c/status)](https://codeship.io/projects/33458)


		



	

