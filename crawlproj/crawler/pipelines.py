# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from crawler.models import Course_info, Inst_info

class course_pipeline(object):
    def process_item(self, item, spider):
        print(f'process_item in pipeline: title={item["title"]}')
        print(f"course_id = {item['course_id']}")
        print(f"inst_nm = {item['org']}")
        #inst_info = Inst_info.objects.get(inst_nm=item['org'])
        '''
        try:
            inst_info = Inst_info.objects.get(inst_nm=item['org'])
        except:
            inst_info = None
        '''
        keyheader = spider.keyheader
        course_id = keyheader + item['course_id']

        # 유효성 체크
        # db 등록
        course_info,flag = Course_info.objects.get_or_create(course_id=course_id)
        course_info.course_nm = item['title']
        course_info.tag = item['org']      #기관명은 tag field에 저장
        # 나머지 항목들 추가
        course_info.save()

        return item

class inst_pipeline(object):
    def process_item(self, item, spider):
        print(f'process_item in pipeline: id={item["inst_id"]}, title={item["inst_nm"]}')
        keyheader = spider.keyheader
        inst_id = keyheader + item['inst_id']

        # db 등록
        inst_info,flag = Inst_info.objects.get_or_create(inst_id=inst_id)
        inst_info.inst_nm = item['inst_nm']
        # 나머지 항목들 추가
        inst_info.save()

        return item
