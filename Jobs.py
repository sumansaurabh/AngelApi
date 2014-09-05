#!/usr/bin/python
import json, urllib
class Jobs:
    'Common base class for all Jobs'
    id=0;
    title= "";
    created_at="";
    updated_at="";
    equity_cliff="";
    equity_min="";
    equity_max="";
    equity_vest="";
    salary_min="";
    salary_max="";
    job_type=""; 
    angellist_url="";
    startup_id="";
    startup_hidden="";
    startup_name="";
    startup_angellist_url= "",
    startup_logo_url="";
    startup_thumb_url="";
    startup_product_desc="";
    startup_high_concept="";
    startup_follower_count="";
    startup_company_url=""

    location=""
    skilltags=[];

   
   

   