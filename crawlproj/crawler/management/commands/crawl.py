from django.core.management.base import BaseCommand
#from scraper.spiders import TheodoSpider
from crawlproj.celery import ulsan_course_task
from crawlproj.celery import ulsan_inst_task
from crawlproj.celery import gangwon_inst_task
from crawlproj.celery import gyeongbuk_inst_task
from crawlproj.celery import gangwon_course_task
from crawlproj.celery import gyeongbuk_course_task

class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        #ulsan_course_task()
        #ulsan_inst_task()
        #gangwon_inst_task()
        #gangwon_course_task()
        gyeongbuk_inst_task()
        #gyeongbuk_course_task()