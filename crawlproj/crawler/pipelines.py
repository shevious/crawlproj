# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from crawler.models import Course_info

class course_pipeline(object):
    def process_item(self, item, spider):
        print(f'process_item in pipeline: title={item["title"]}')
        # task_id 를 추가저장
        task_id = spider.task_id
        # 유효성 체크

        # db 등록
        course_info = Course_info()
        course_info.task_id = task_id
        course_info.course_nm = item['title']
        course_info.save()
        
        return item


from crawler.models import Inst_info

class inst_pipeline(object):
    def process_item(self, item, spider):
        print(f'process_item in pipeline: title={item["inst_nm"]}')
        # task_id 를 추가저장
        task_id = spider.task_id
        # 유효성 체크

        # db 등록
        inst_info = Inst_info()
        inst_info.task_id = task_id
        inst_info.inst_nm = item['inst_nm']
        inst_info.inst_id = item['inst_id']
        inst_info.save()

        return item