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

from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from scrapy.spiderloader import SpiderLoader

from crochet import setup, wait_for
from scrapy.utils.log import configure_logging
from celery.platforms import signals

from celery import current_task
import uuid

@wait_for(timeout=99999)
def run_spider(settings, keyheader=''):
    s = Settings()
    s.setmodule(settings)
    sl = SpiderLoader(settings=s)
    print('spider list=', sl.list())
    spider = sl.load(sl.list()[0])
    configure_logging({'LOG_LEVEL': 'DEBUG'}) # scrapy 로그 레벨 설정
    runner = CrawlerRunner(settings=s)
    d = runner.crawl(spider, keyheader=keyheader)
    return d

# 헤더 정보 및 고유값
keyheaders = {
    "ulsan": "UL"
}

# 울산 강좌 정보
from Ulsan import settings as ulsan_settings

@app.task(bind=True)
def ulsan_course_task(self):
    task_id = current_task.request.id
    if task_id is None:
        task_id = uuid.uuid1()
    print(f'############# task started: task_id = {task_id}')
    keystring = "ulsan"

    from crawler.models import Course_info

    #task_log = Task_log(task_id = task_id, name = 'ulsan_course')
    #task_log.save()

    settings = ulsan_settings
    settings.ITEM_PIPELINES = {
        'crawler.pipelines.course_pipeline': 300,
    }
    #settings.DOWNLOAD_DELAY = 1.0 # 다운로드 지연(디버깅용)

    setup()
    d = run_spider(settings, keyheader=keyheaders[keystring])
    #task_log.total_cnt = Course_info.objects.filter(task_id=task_id).count()
    #task_log.status = 'success'
    #task_log.save()

    print('############## task ended')


# 울산 기관 정보
from UlsanInst import settings as ulsaninst_settings

@app.task(bind=True)
def ulsan_inst_task(self):
    task_id = current_task.request.id
    if task_id is None:
        task_id = uuid.uuid1()
    print(f'############# task started: task_id = {task_id}')
    keystring = "ulsan"

    from crawler.models import Inst_info

    settings = ulsaninst_settings
    settings.ITEM_PIPELINES = {
        'crawler.pipelines.inst_pipeline': 300,
    }
    #settings.DOWNLOAD_DELAY = 1.0 # 다운로드 지연(디버깅용)

    setup()
    d = run_spider(settings, keyheader=keyheaders[keystring])

    print('############## task ended')
