sgBeat Scraper
==============

This is a Scrapy-based scraper for sgbeat.com. Is designed to grab tweets and store it in a MySQL database with schema as defined in schema.sql. Included in database.py is Tornado's MySQL database wrapper.

Dependencies:

	Scrapy
	MySQLdb (the Python wrapper for MySQL)

Remember to create a details.py file with the following details:

	HOST_NAME = ""
	MYSQL_DB_NAME = ""
	MYSQL_USER_NAME = ""
	MYSQL_PASSWORD = ""

This code is used in a IEM2201D research project - to build a classifier for Singaporean vs Malaysian tweets. Due to sgBeat's unique nature, all tweets pushed to the site are Singaporean, thus making for a good source for a Singaporean corpus.