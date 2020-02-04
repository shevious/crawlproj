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
import logging
from scrapy import signals

class SigHandler(object):
    def __init__(self):
        self.item_scraped_count = 0
        #self.crawler = None

    def connect(self, crawler):
        #print('###### signal connect')
        #crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def spider_closed(self, spider):
        #print('###### spider closed')
        pass

    def item_scraped(self, item, spider):
        #print('###### item scraped signal')
        self.item_scraped_count += 1

class ItemCount(object):
    def __init__(self):
        self.item_scraped_count = 0

@wait_for(timeout=99999)
#def run_spider(settings, sighandler, keyheader='', conid=''):
def run_spider(settings, itemcount, keyheader='', conid=''):
    s = Settings()
    s.setmodule(settings)
    sl = SpiderLoader(settings=s)
    print('spider list=', sl.list())
    spider = sl.load(sl.list()[0])
    spider.itemcount = itemcount
    configure_logging({'LOG_LEVEL': 'DEBUG'}) # scrapy 로그 레벨 설정
    runner = CrawlerRunner(settings=s)

    crawler = runner.create_crawler(spider)
    #if sighandler != None:
        #sighandler.connect(crawler)
    d = runner.crawl(crawler, keyheader=keyheader, conid=conid)
    #d = runner.crawl(spider, keyheader=keyheader, itemcount=itemcount)
    return d

# 헤더 정보 및 고유값
# 아레 header값을 course_id나 inst_id앞에 붙여서 저장함.
keyheaders = {
    "ulsan": "UL",
    "gangwon": "GW",
    "gyeongbuk": "GB",
}
conids = {
    "ulsan": "31",
    "gangwon": "42",
    "gyeongbuk": "47",
}
conids_course = {
    "ulsan": "76",
    "gangwon": "74",
    "gyeongbuk": "78",
}

from datetime import date, datetime
#from pytz import timezone
from django.utils import timezone
from time import strftime

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
    con_log.con_id = conids_course[keystring]
    con_log.con_tm = datetime.now().strftime('%H:%M')
    con_log.con_kind_cd = 'COURSE_CRL'
    con_log.save()
    print(f'##### max_log_id = {con_log_id}')

    settings = ulsan_settings
    settings.ITEM_PIPELINES = {
        'crawler.pipelines.course_pipeline': 300,
    }
    #settings.DOWNLOAD_DELAY = 1.0 # 다운로드 지연(디버깅용)

    #settings.LOG_FILE = 'ulsan_course_logfile.log'
    #settings.LOG_LEVEL = logging.ERROR

    setup()
    #sighandler = SigHandler()
    #d = run_spider(settings, sighandler=sighandler, keyheader=keyheaders[keystring], conid=conids[keystring])
    itemcount = ItemCount()
    d = run_spider(settings, itemcount=itemcount, keyheader=keyheaders[keystring], conid=conids_course[keystring])
    con_log.reg_dt = timezone.now()
    #con_log.log_desc = f'total count = {sighandler.item_scraped_count}'
    con_log.log_desc = f'total count = {itemcount.item_scraped_count}'
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
    from django.db.models import Max

    settings = ulsaninst_settings
    settings.ITEM_PIPELINES = {
        'crawler.pipelines.inst_pipeline': 300,
    }
    #settings.DOWNLOAD_DELAY = 1.0 # 다운로드 지연(디버깅용)
    maxid = Con_log.objects.aggregate(Max('con_log_id'))
    con_log_id = str(int('9' + maxid['con_log_id__max']) + 1)[1:]
    con_log = Con_log(con_log_id=con_log_id)
    con_log.con_id = conids[keystring]
    con_log.con_tm = datetime.now().strftime('%H:%M')
    con_log.con_kind_cd = 'INSTI_CRL'
    con_log.save()
    print(f'##### max_log_id = {con_log_id}')

    setup()
    sighandler = SigHandler()
    itemcount = ItemCount()
    #d = run_spider(settings, sighandler=sighandler, keyheader=keyheaders[keystring], conid=conids[keystring])
    d = run_spider(settings, itemcount=itemcount, keyheader=keyheaders[keystring], conid=conids[keystring])
    con_log.reg_dt = timezone.now()
    #con_log.log_desc = f'total count = {sighandler.item_scraped_count}'
    con_log.log_desc = f'total count = {itemcount.item_scraped_count}'
    con_log.con_status_cd = 'SUCCESS'
    con_log.save()
    print('############## task ended')

# 강원 기관 정보
from GangwonInst import settings as gangwonInst_settings

@app.task(bind=True)
def gangwon_inst_task(self):
    task_id = current_task.request.id
    if task_id is None:
        task_id = uuid.uuid1()
    print(f'############# task started: task_id = {task_id}')
    keystring = "gangwon"

    from crawler.models import Inst_info, Con_log
    from django.db.models import Max

    maxid = Con_log.objects.aggregate(Max('con_log_id'))
    con_log_id = str(int('9' + maxid['con_log_id__max']) + 1)[1:]
    con_log = Con_log(con_log_id=con_log_id)
    con_log.con_id = conids[keystring]
    con_log.con_tm = datetime.now().strftime('%H:%M')
    con_log.con_kind_cd = 'INSTI_CRL'
    con_log.save()
    print(f'##### max_log_id = {con_log_id}')

    settings = gangwonInst_settings
    settings.ITEM_PIPELINES = {
        'crawler.pipelines.inst_pipeline': 300,
    }
    #settings.DOWNLOAD_DELAY = 1.0 # 다운로드 지연(디버깅용)

    setup()
    #sighandler = SigHandler()
    itemcount = ItemCount()
    #d = run_spider(settings, sighandler=sighandler, keyheader=keyheaders[keystring], conid=conids[keystring])
    d = run_spider(settings, itemcount=itemcount, keyheader=keyheaders[keystring], conid=conids[keystring])
    con_log.reg_dt = timezone.now()
    #con_log.log_desc = f'total count = {sighandler.item_scraped_count}'
    con_log.log_desc = f'total count = {itemcount.item_scraped_count}'
    con_log.con_status_cd = 'SUCCESS'
    con_log.save()
    print('############## task ended')

# 강원 강좌 정보
from Gangwon import settings as gangwon_settings

@app.task(bind=True)
def gangwon_course_task(self):
    task_id = current_task.request.id
    if task_id is None:
        task_id = uuid.uuid1()
    print(f'############# task started: task_id = {task_id}')
    keystring = "gangwon"

    from crawler.models import Course_info, Con_log
    from django.db.models import Max

    #task_log = Task_log(task_id = task_id, name = 'ulsan_course')
    #task_log.save()
    maxid = Con_log.objects.aggregate(Max('con_log_id'))
    con_log_id = str(int('9' + maxid['con_log_id__max']) + 1)[1:]
    con_log = Con_log(con_log_id=con_log_id)
    con_log.con_id = conids_course[keystring]
    con_log.con_tm = datetime.now().strftime('%H:%M')
    con_log.con_kind_cd = 'COURSE_CRL'
    con_log.save()
    print(f'##### max_log_id = {con_log_id}')

    settings = gangwon_settings
    settings.ITEM_PIPELINES = {
        'crawler.pipelines.course_pipeline': 300,
    }
    #settings.DOWNLOAD_DELAY = 1.0 # 다운로드 지연(디버깅용)
    #settings.LOG_FILE = 'gangwon_course_logfile.log'
    setup()
    #sighandler = SigHandler()
    itemcount = ItemCount()
    #d = run_spider(settings, sighandler=sighandler, keyheader=keyheaders[keystring], conid=conids[keystring])
    d = run_spider(settings, itemcount=itemcount, keyheader=keyheaders[keystring], conid=conids_course[keystring])
    con_log.reg_dt = timezone.now()
    #con_log.log_desc = f'total count = {sighandler.item_scraped_count}'
    con_log.log_desc = f'total count = {itemcount.item_scraped_count}'
    con_log.con_status_cd = 'SUCCESS'
    con_log.save()

    print('############## task ended')


# 경북 기관 정보
from GyeongbukInst import settings as gyeongbukinst_settings

@app.task(bind=True)
def gyeongbuk_inst_task(self):
    task_id = current_task.request.id
    if task_id is None:
        task_id = uuid.uuid1()
    print(f'############# task started: task_id = {task_id}')
    keystring = "gyeongbuk"

    from crawler.models import Inst_info, Con_log
    from django.db.models import Max

    maxid = Con_log.objects.aggregate(Max('con_log_id'))
    con_log_id = str(int('9' + maxid['con_log_id__max']) + 1)[1:]
    con_log = Con_log(con_log_id=con_log_id)
    con_log.con_id = conids[keystring]
    con_log.con_tm = datetime.now().strftime('%H:%M')
    con_log.con_kind_cd = 'INSTI_CRL'
    con_log.save()
    print(f'##### max_log_id = {con_log_id}')

    settings = gyeongbukinst_settings
    settings.ITEM_PIPELINES = {
        'crawler.pipelines.inst_pipeline': 300,
    }
    #settings.DOWNLOAD_DELAY = 1.0 # 다운로드 지연(디버깅용)

    setup()
    #sighandler = SigHandler()
    itemcount = ItemCount()
    #d = run_spider(settings, sighandler=sighandler, keyheader=keyheaders[keystring], conid=conids[keystring])
    d = run_spider(settings, itemcount=itemcount, keyheader=keyheaders[keystring], conid=conids[keystring])
    con_log.reg_dt = timezone.now()
    #con_log.log_desc = f'total count = {sighandler.item_scraped_count}'
    con_log.log_desc = f'total count = {itemcount.item_scraped_count}'
    con_log.con_status_cd = 'SUCCESS'
    con_log.save()
    print('############## task ended')

# 울산 강좌 정보
from Gyeongbuk import settings as gyeongbuk_settings

@app.task(bind=True)
def gyeongbuk_course_task(self):
    task_id = current_task.request.id
    if task_id is None:
        task_id = uuid.uuid1()
    print(f'############# task started: task_id = {task_id}')
    keystring = "gyeongbuk"

    from crawler.models import Course_info, Con_log
    from django.db.models import Max

    #task_log = Task_log(task_id = task_id, name = 'ulsan_course')
    #task_log.save()
    maxid = Con_log.objects.aggregate(Max('con_log_id'))
    con_log_id = str(int('9' + maxid['con_log_id__max']) + 1)[1:]
    con_log = Con_log(con_log_id=con_log_id)
    con_log.con_id = conids_course[keystring]
    con_log.con_tm = datetime.now().strftime('%H:%M')
    con_log.con_kind_cd = 'COURSE_CRL'
    con_log.save()
    print(f'##### max_log_id = {con_log_id}')

    settings = gyeongbuk_settings
    settings.ITEM_PIPELINES = {
        'crawler.pipelines.course_pipeline': 300,
    }
    #settings.DOWNLOAD_DELAY = 1.0 # 다운로드 지연(디버깅용)
    #settings.LOG_FILE = 'gyeongbuk_course_logfile.log'
    #settings.LOG_LEVEL = logging.ERROR

    setup()
    #sighandler = SigHandler()
    itemcount = ItemCount()
    #d = run_spider(settings, sighandler=sighandler, keyheader=keyheaders[keystring], conid=conids[keystring])
    d = run_spider(settings, itemcount=itemcount, keyheader=keyheaders[keystring], conid=conids_course[keystring])
    con_log.reg_dt = timezone.now()
    #con_log.log_desc = f'total count = {sighandler.item_scraped_count}'
    con_log.log_desc = f'total count = {itemcount.item_scraped_count}'
    con_log.con_status_cd = 'SUCCESS'
    con_log.save()
    print('############## task ended')
