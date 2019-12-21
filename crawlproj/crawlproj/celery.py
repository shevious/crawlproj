from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocelery.settings')

app = Celery('djangocelery',
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

'''
#@app.task(bind=True)
@app.task
def add(x, y):
    print("{} + {} = {}".format(x, y, x+y))
    return (x+y)

from time import sleep
from celery.contrib.abortable import AbortableTask

from celery.signals import worker_shutting_down

@worker_shutting_down.connect
def worker_shutting_down_handler(sig, how, exitcode, ** kwargs):
    print(f'worker_shutting_down({sig}, {how}, {exitcode})')

@app.task(bind=True, base=AbortableTask)
def longtask(self):
    from celery.platforms import signals
    from celery.contrib.abortable import AbortableAsyncResult

    def int_handler(signum, frame):
        id = self.request.id
        print(f'##### int_handler({signum}, {frame})')
        print(f'##### id = {id}')
        result = AbortableAsyncResult(id)
        result.abort()

    signals['TERM'] = int_handler
    #signals['INT'] = int_handler

    for i in range(0, 6):
        if self.is_aborted():
            return 'aborted'
        print('sleeping 3 seconds')
        sleep(3)
    return 'completed'
'''

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

default_handler = signals['TERM']

@app.task(bind=True)
def ulsan_course_task(self, base=AbortableTask):
    '''
    from celery.contrib.abortable import AbortableAsyncResult

    def int_handler(signum, frame):
        #global default_handler
        id = self.request.id
        print('############## int_handler')
        print(f'int_handler({signum}, {frame})')
        print(f'id = {id}')
        #print(f'process = {this.process}')
        print('############## int_handler')
        #result = AbortableAsyncResult(id)
        #result.abort()
        # default_handler(signum, frame)
        return

    print(f"##### term handler = {signals['TERM']}")
    '''
    #signals['INT'] = int_handler
    #signals['TERM'] = int_handler

    setup()

    @wait_for(timeout=99999)
    def run_spider():
        s = Settings()
        s.setmodule(ulsan_settings)
        #process = CrawlerProcess(get_project_settings())
        sl = SpiderLoader(settings=s)
        print('#### spider list=', sl.list())
        spider = sl.load(sl.list()[0])
        #process = CrawlerProcess(settings=s)
        #d = process.crawl(spider)
        #process.crawl(UillOrKr)
        #process.start(stop_after_crawl=False)
        #process.start()
        #configure_logging({'LOG_FORMAT': '## %(levelname)s: %(message)s'})
        #configure_logging({'LOG_LEVEL': 'DEBUG'})
        runner = CrawlerRunner(settings=s)
        print(f'#### settings.LOG_ENABLED = {s["LOG_ENABLED"]}')
        d = runner.crawl(spider)
        #d.addBoth(lambda _: reactor.stop())
        #reactor.run()
        #return d
        return d

    d = run_spider()
    print('##############')
