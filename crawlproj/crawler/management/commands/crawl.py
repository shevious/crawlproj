from django.core.management.base import BaseCommand
#from scraper.spiders import TheodoSpider
from crawlproj.celery import ulsan_course_task

class Command(BaseCommand):
    help = "Release the spiders"

    def handle(self, *args, **options):
        ulsan_course_task()
