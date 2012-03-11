# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import re
from database import Connection
from details import (
		HOST_NAME,
		MYSQL_DB_NAME,
		MYSQL_USER_NAME,
		MYSQL_PASSWORD
	)

class SgbeatPipeline(object):
    def process_item(self, item, spider):
    	"""For each item, check if uname exists.
    	Write tweet to database
    	"""
    	db = Connection(host = HOST_NAME,
    					database = MYSQL_DB_NAME,
    					user = MYSQL_USER_NAME,
    					password = MYSQL_PASSWORD)

    	tweet = db.escape_string(item["tweet"])

    	user = db.get("SELECT id from users WHERE username='%s';" % item["username"])
    	twt = db.get("SELECT * from tweets WHERE tweet='%s';" % tweet)
    	if not twt:
    		if user:
    			db.execute("INSERT into tweets (user, tweet) VALUES ('%s', '%s');" % (user["id"], tweet))
    		else:
    			db.execute("INSERT into users (username) VALUES ('%s');" % item["username"])
    			user = db.get("SELECT id from users WHERE username='%s';" % item["username"])
    			db.execute("INSERT into tweets (user, tweet) VALUES ('%s', '%s');" % (user["id"], tweet))

    	db.close()
        return item
