# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from crawler.models import Course_info, Inst_info, Con_log

class course_pipeline(object):
    def process_item(self, item, spider):
        print(f'process_item in pipeline: title={item["course_nm"]}')
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
        #itemcount = spider.itemcount
        conid = spider.conid
        #print(f'itemcount = {itemcount.item_scarped_count}')
        #itemcount.item_scarped_count += 1
        course_id = keyheader + item['course_id']

        # 유효성 체크
        # db 등록
        course_info,flag = Course_info.objects.get_or_create(course_id=course_id, con_id=conid)
        course_info.course_nm = item['course_nm']
        course_info.tag = item['org']      #기관명은 tag field에 저장
        course_info.con_id = conid
        # 나머지 항목들 추가
        course_info.course_start_dt = item['course_start_dt']
        course_info.course_end_dt = item['course_end_dt']
        course_info.receive_start_dt = item['receive_start_dt']
        course_info.receive_end_dt = item['receive_end_dt']
        course_info.teacher_pernm = item['teacher_pernm']
        course_info.enroll_amt = item['enroll_amt']
        course_info.edu_method_cd = item['edu_method_cd']      # 교육방법CD
        course_info.edu_target_cd = item['edu_target_cd']       # 교육대상CD
        course_info.edu_cycle_content = item['edu_cycle_content']  # 교육주기
        course_info.edu_quota_cnt = item['edu_quota_cnt']  # 교육정원
        course_info.edu_location_desc = item['edu_location_desc']  # 교육장소
        course_info.inquiry_tel_no = item['inquiry_tel_no']  # 교육문의전화
        course_info.enroll_appl_method_cd = item['enroll_appl_method_cd']  # 수강신청방법
        course_info.link_url = item['link_url']  # URl
        course_info.course_desc = item['course_desc']  # 교육설명
        course_info.job_ability_course_yn = item['job_ability_course_yn']  # 직업능력개발훈련비지원여부
        course_info.cb_eval_accept_yn = item['cb_eval_accept_yn']  # 학점은행제평가인정여부
        course_info.all_eval_accept_yn = item['all_eval_accept_yn']  # 평생학습계좌제평가인정기관여부
        course_info.lang_cd = item['lang_cd']  # 언어
        course_info.vsl_handicap_supp_yn = item['vsl_handicap_supp_yn']  # 시각장애지원여부
        course_info.hrg_handicap_supp_yn = item['hrg_handicap_supp_yn']  # 청각장애지원여부
        course_info.save()

        return item

class inst_pipeline(object):
    def process_item(self, item, spider):
        print(f'process_item in pipeline: id={item["inst_id"]}, title={item["inst_nm"]}')
        keyheader = spider.keyheader
        #itemcount = spider.itemcount
        conid = spider.conid
        #print(f'itemcount = {itemcount.item_scarped_count}')
        #itemcount.item_scarped_count += 1
        inst_id = keyheader + item['inst_id']

        # db 등록
        inst_info,flag = Inst_info.objects.get_or_create(inst_id=inst_id, con_id=conid)
        inst_info.inst_nm = item['inst_nm']
        inst_info.tag = item['inst_nm']
        inst_info.con_id = conid
        # 나머지 항목들 추가
        inst_info.inst_ceo_pernm = item['inst_ceo_pernm']
        inst_info.inst_set_up_main_agent_cd = item['inst_set_up_main_agent_cd']   # 기관설립주체코드
        inst_info.inst_operation_form_cd = item['inst_operation_form_cd']  # 기관운영형태코드
        inst_info.zipcode = item['zipcode']
        inst_info.addr1 = item['addr1']
        inst_info.tel_no = item['tel_no']
        inst_info.fax_no = item['fax_no']
        inst_info.email = item['email']
        inst_info.homepage_url = item['homepage_url']
        inst_info.inst_desc = item['inst_desc']
        inst_info.establishment_dt = item['establishment_dt']
        inst_info.inst_operation_status_cd = item['inst_operation_status_cd'] # 기관운영상태코드
        inst_info.save()

        return item
