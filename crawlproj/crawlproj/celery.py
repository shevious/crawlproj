from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crawlproj.settings')

app = Celery('crawlproj',
             #broker='amqp://',
             #backend='amqp://',
            )

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

#app.log.setup_task_loggers(loglevel='DEBUG')

#from celery.signals import setup_logging

#@setup_logging.connect
#def config_loggers(*args, **kwags):
#    from logging.config import dictConfig
#    from django.conf import settings
#    dictConfig(settings.LOGGING)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

from Ulsan.spiders.uill_or_kr import UillOrKr
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from Ulsan import settings as ulsan_settings
from scrapy.spiderloader import SpiderLoader

from crochet import setup, wait_for
from scrapy.utils.log import configure_logging
from celery.platforms import signals

from celery import current_task
import uuid

#default_handler = signals['TERM']

@app.task(bind=True)
def ulsan_course_task(self):
    try:
        setup()
    except:
        pass

    task_id = current_task.request.id
    if task_id is None:
        task_id = uuid.uuid1()

    print(f'############# task started = {task_id}')

    @wait_for(timeout=99999)
    def run_spider():
        s = Settings()
        s.setmodule(ulsan_settings)
        #process = CrawlerProcess(get_project_settings())
        sl = SpiderLoader(settings=s)
        print('spider list=', sl.list())
        spider = sl.load(sl.list()[0])
        #process = CrawlerProcess(settings=s)
        #d = process.crawl(spider)
        #process.crawl(UillOrKr)
        #process.start(stop_after_crawl=False)
        #process.start()
        #configure_logging({'LOG_FORMAT': '## %(levelname)s: %(message)s'})
        #configure_logging({'LOG_LEVEL': 'DEBUG'})
        runner = CrawlerRunner(settings=s)
        #print(f'#### settings.LOG_ENABLED = {s["LOG_ENABLED"]}')
        d = runner.crawl(spider, task_id=task_id)
        #d.addBoth(lambda _: reactor.stop())
        #reactor.run()
        #return d
        return d

    d = run_spider()
    print('############## task ended')
