#!/usr/bin/env python

from google.appengine.ext import db

# These classes define the data objects
# that you will be able to store in
# AppEngine's data store.

class KeywordTags(db.Model):
#	keyword = db.StringProperty(required=True, indexed=True)
	jobids = db.ListProperty(int)


class LocationTags(db.Model):
#	location = db.StringProperty(required=True, indexed=True)
	jobids = db.ListProperty(int)