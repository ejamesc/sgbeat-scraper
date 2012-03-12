import re

from scrapy.spider import BaseSpider
from sgbeat.items import SgbeatItem
from scrapy.selector import HtmlXPathSelector

def strip_tags(value):
	"""Returns given HTML with all tags stripped."""
	return re.sub(r'<[^>]*?>', '', value)

def strip_tweet(value):
	"""Returns just the content of the tweet
	Takes:
		AmandaMeow: I love you. 0 min ago via SMS
	and returns:
		I love you.
	"""
	res = re.sub(r'^\w*:', '', value)
	res = re.sub(r'\d* hr, \d* min ago via \w*$', '', res)
	return re.sub(r'\d* min ago via \w*$', '', res)

class SGbeatSpider(BaseSpider):
	name = "sgbeat"
	allowed_domains = ["sgbeat.com"]
	start_urls = [
		"http://sgbeat.com/"
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		unames = hxs.select("//div[@id='beats']/ul[1]/li/div[contains(concat(' ',@class,' '),' msg ')]/strong[1]/a[1]").extract()
		rawtweets = hxs.select("//div[@id='beats']/ul[1]/li/div[contains(concat(' ',@class,' '),' msg ')]").extract()

		unames = [strip_tags(u) for u in unames]
		rawtweets = [strip_tags(r) for r in rawtweets]
		rawtweets = [' '.join([s.strip() for s in r.split()]) for r in rawtweets]
		rawtweets = [strip_tweet(r).strip() for r in rawtweets]
		tweets = []
		x = 0

		for u in unames:
			item = SgbeatItem()
			item['username'] = u
			item['tweet'] = rawtweets[x]
			tweets.append(item)
			x = x+1

		return tweets