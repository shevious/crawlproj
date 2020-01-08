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

    def add_arguments(self, parser):
        parser.add_argument('task', type=str, help='ulsan_course, ulsan_inst, gangwon_course...')

    def handle(self, *args, **kwargs):
        print(kwargs['task'])
        if kwargs['task'] == 'ulsan_course':
            ulsan_course_task()
        elif kwargs['task'] == 'ulsan_inst':
            ulsan_inst_task()
        elif kwargs['task'] == 'gangwon_course':
            gangwon_course_task()
        elif kwargs['task'] == 'gangwon_inst':
            gangwon_inst_task()
        elif kwargs['task'] == 'gyeongbuk_inst':
            gyeongbuk_inst_task()
        elif kwargs['task'] == 'gyeongbuk_course':
            gyeongbuk_course_task()
        else:
            print('Usage: ./manage.py crawl <task_name>')
