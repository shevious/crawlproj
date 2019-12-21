# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from crawler.models import Course_info

'''
from scrapy_djangoitem import DjangoItem
class CourseItem(DjangoItem):
    django_model = Course_info
'''

class UlsanPipeline(object):
    def process_item(self, item, spider):
        print(f'process_item in pipeline: title={item["title"]}')
        # 유효성 체크

        # db 등록
        #course_item = CourseItem()
        #course_item['course_nm'] = item['title']
        #course_item.save()

        course_info = Course_info()
        course_info.course_nm = item['title']
        course_info.save()
        
        return item
