# Scrapy settings for sgbeat project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'sgbeat'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['sgbeat.spiders']
NEWSPIDER_MODULE = 'sgbeat.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
	'sgbeat.pipelines.SgbeatPipeline',
]