[AngelList Api](http://angel.co/)

#### Work Flow
	
	1) Run in Terminal dev_appserver.py <folder_location>
	2) Open browser - localhost:8080
	4) Keyword (Skills / Company Name ) and Location: Enter the details
	5) Database shows the jobs
		a. Keyword and Location -- At the top
		b. Only Keyword 	-- At middle
		c. Only Location 	-- At bottom

#### Process (Cron Job used to update database at 12:00)
1) https://api.angel.co/1/jobs?page=1 to 50 job datas are availabe. 
2) localhost:8080/cron fetches each job from each page and builds a data-store for Location and Keyword containing corresponding job-ids, containing only Business related jobs (they are segregated using their Role-Tags).
Google app engine has a tool called memcache which stores the job in memory(like RAM).
	<keyword: {job-ids list} >
	<location: {job-ids list} >
	eg. Skill_Table would contain: 
		<sales: {3350, 4234, 5263}> - 
	eg. Location_Table would contain: 
		<Boston : {4234,3350,93214}>

			Results would be:
		a) Using both tags: Jobs with id: {4234,3350}
		b) Only using location tag : {93214}
		c) Only using Keyword tag :	{5263}

#### Note
Currently only 3 pages are being loaded, all pages request would be made soon availabe.


