from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'
    
    def handle(self, *args, **options):
        from scrapy import signals
        from scrapy.xlib.pydispatch import dispatcher
        
        def catch_item(sender, item, **kwargs):
            print "Got:", item
            
        dispatcher.connect(catch_item, signal=signals.item_passed)
        
        from scrapy.conf import settings
        settings.overrides['LOG_ENABLED'] = True
        
        from scrapy.crawler import CrawlerProcess
        
        crawler = CrawlerProcess(settings)
        crawler.install()
        crawler.configure()
        
        from alescspider.spiders import *
        spiders = [deputado_spider.DeputadoSpider()]
        #spiders = [presenca_spider.PresencaSpider(), votos_spider.VotosSpider(), deputado_spider.DeputadoSpider()]
        for spider in spiders:
            crawler.queue.append_spider(spider)
        
        print "STARTING ENGINE"
        crawler.start()
        print "ENGINE STOPPED"
        