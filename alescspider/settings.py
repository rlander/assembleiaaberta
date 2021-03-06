# Scrapy settings for alesc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'alesc'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['alescspider.spiders']
NEWSPIDER_MODULE = 'alescspider.spiders'
DEFAULT_ITEM_CLASS = 'alescspider.items.AlescItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = ['alescspider.pipelines.JsonExportPipeline']

#ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline']
#IMAGES_STORE = '/vagrant/alesc-web/alesc/images'
