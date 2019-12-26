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

from scrapy import signals

class ItemCount(object):
    def __init__(self):
        self.item_scarped_count = 0

@wait_for(timeout=99999)
def run_spider(settings, keyheader='', itemcount=None):
    s = Settings()
    s.setmodule(settings)
    sl = SpiderLoader(settings=s)
    print('spider list=', sl.list())
    spider = sl.load(sl.list()[0])
    configure_logging({'LOG_LEVEL': 'DEBUG'}) # scrapy 로그 레벨 설정
    runner = CrawlerRunner(settings=s)
    #crawler = runner.create_crawler(spider)
    #crawler.signals.connect(scraped, signal=signals.item_scraped)
    #d = runner.crawl(crawler, keyheader=keyheader, itemcount=itemcount)
    d = runner.crawl(spider, keyheader=keyheader, itemcount=itemcount)
    return d

# 헤더 정보 및 고유값
# 아레 header값을 course_id나 inst_id앞에 붙여서 저장함.
keyheaders = {
    "ulsan": "UL",
    "gangwon": "GW",
    "gyeongbuk": "GB",
}
conids = {
    "ulsan": "01",
    "gangwon": "02",
    "gyeongbuk": "03",
}


from datetime import date

# 울산 강좌 정보
from Ulsan import settings as ulsan_settings

@app.task(bind=True)
def ulsan_course_task(self):
    task_id = current_task.request.id
    if task_id is None:
        task_id = uuid.uuid1()
    print(f'############# task started: task_id = {task_id}')
    keystring = "ulsan"

    from crawler.models import Course_info, Con_log
    from django.db.models import Max

    #task_log = Task_log(task_id = task_id, name = 'ulsan_course')
    #task_log.save()
    maxid = Con_log.objects.aggregate(Max('con_log_id'))
    con_log_id = str(int('9' + maxid['con_log_id__max']) + 1)[1:]
    con_log = Con_log(con_log_id=con_log_id)
    con_log.con_id = conids[keystring]
    con_log.save()
    print(f'##### max_log_id = {con_log_id}')

    settings = ulsan_settings
    settings.ITEM_PIPELINES = {
        'crawler.pipelines.course_pipeline': 300,
    }
    #settings.DOWNLOAD_DELAY = 1.0 # 다운로드 지연(디버깅용)

    setup()
    itemcount = ItemCount()
    d = run_spider(settings, keyheader=keyheaders[keystring], itemcount=itemcount)
    #task_log.total_cnt = Course_info.objects.filter(task_id=task_id).count()
    #task_log.status = 'success'
    #task_log.save()
    con_log.reg_dt = date.today()
    con_log.log_desc = f'total count'
    con_log.con_status_cd = 'SUCCESS'
    con_log.save()

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

    from crawler.models import Inst_info, Con_log

    settings = ulsaninst_settings
    settings.ITEM_PIPELINES = {
        'crawler.pipelines.inst_pipeline': 300,
    }
    #settings.DOWNLOAD_DELAY = 1.0 # 다운로드 지연(디버깅용)

    setup()
    d = run_spider(settings, keyheader=keyheaders[keystring])

    print('############## task ended')
