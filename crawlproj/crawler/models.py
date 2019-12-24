
from django.db import models

class Course_info(models.Model):
    course_id = models.CharField(max_length=200)
    inst_id = models.CharField(null=True, max_length=200)
    total_cd = models.CharField(null=True, max_length=10) # length correct?
    sido_cd = models.CharField(null=True, max_length=10)
    sigungu_cd = models.CharField(null=True, max_length=10)
    course_nm = models.CharField(null=True, max_length=400)
    course_desc_url = models.CharField(null=True, max_length=2000) 
    course_pttn_cd = models.CharField(null=True, max_length=2)
    extra_charge_content = models.CharField(null=True, max_length=200)
    edu_cycle_content = models.CharField(null=True, max_length=200)
    edu_quota_cnt = models.CharField(null=True, max_length=200) # why NVARCHAR2?
    course_start_dt = models.DateField(null=True)
    course_end_dt = models.DateField(null=True)
    receive_start_dt = models.DateField(null=True)
    receive_end_dt = models.DateField(null=True)
    edu_tm = models.CharField(null=True, max_length=200)
    edu_location_desc = models.CharField(null=True, max_length=2000)
    inquiry_tel_no = models.CharField(null=True, max_length=100)
    #teacher_pernm = models.CharField(max_length=200)
    #info_mng_inst_id = models.CharField(max_length=100)
    #info_inp_inst_id = models.CharField(max_length=100)
    reg_user_id = models.CharField(null=True, max_length=30)
    reg_dt = models.DateField(null=True)
    #upd_user_id = models.CharField(max_length=30)
    upd_dt = models.DateField(null=True)
    #tag = models.CharField(max_length=4000)
    '''
    job_ability_course_yn = models.CharField(max_length=1)
    cb_eval_accept_yn = models.CharField(max_length=1)
    #all_eval_accept_yn = models.CharField(max_length=1)
    lang_cd = models.CharField(max_length=10)
    #study_os_nm = models.CharField(max_length=200)
    #study_web_browser_nm = models.CharField(max_length=100)
    #study_device_nm = models.CharField(max_length=100)
    vsl_handicap_supp_yn = models.CharField(max_length=1)
    hrg_handicap_supp_yn = models.CharField(max_length=1)
    course_class1_cd = models.CharField(max_length=2)
    course_class2_cd = models.CharField(max_length=2)
    #course_thumbnail_url = models.CharField(max_length=200)
    edu_target_cd = models.CharField(max_length=200)
    #enroll_appl_method_cd = models.CharField(max_length=10)
    #edu_method_cd = models.CharField(max_length=10)
    edu_lvldff_type_cd =
    ref_book_nm =
    source_desc =
    link_url =
    del_yn =
    course_url =
    course_url_call_method =
    models.CharField(max_length=1)
    models.CharField(max_length=2)
    models.CharField(max_length=10)
    models.CharField(max_length=100)
    models.CharField(max_length=200)
    models.DateField()
    mobile_url =
    mobile_url_call_method =
    course_desc =
    enroll_amt =
    page_cnt =
    page_no =
    total_cnt =
    '''
    task_id = models.CharField(null=True, max_length=100)
    class Meta:
        db_table = "CRAWL_COURSE_INFO"

class Task_log(models.Model):
    task_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=100, default='pending')
    total_cnt = models.CharField(max_length=100, default='0')
    created_at = models.DateTimeField(auto_now_add=True) # 해당 레코드 생성시 현재 시간 자동저장
    updated_at = models.DateTimeField(auto_now=True) # 해당 레코드 갱신시 현재 시간 자동저장
    class Meta:
        db_table = "CRAWL_TASK_LOG"

class Inst_info(models.Model):
    inst_id = models.CharField(null=True, max_length=200)
    total_cd = models.CharField(null=True, max_length=10) # length correct?
    sido_cd = models.CharField(null=True, max_length=10)
    sigungu_cd = models.CharField(null=True, max_length=10)
    inst_nm = models.CharField(null=True, max_length=400)
    inst_ceo_pernm = models.CharField(null=True, max_length=30)
    inst_set_up_main_agent_cd = models.CharField(null=True, max_length=10)
    inst_operation_form_cd = models.CharField(null=True, max_length=10)
    zipcode = models.CharField(null=True, max_length=100)
    addr1 = models.CharField(null=True, max_length=200)
    addr2 = models.CharField(null=True, max_length=200)
    street_cd = models.CharField(null=True, max_length=200)
    street_nm = models.CharField(null=True, max_length=100)
    building_no = models.CharField(null=True, max_length=100)
    detail_addr = models.CharField(null=True, max_length=200)
    manager_pernm = models.CharField(null=True, max_length=200)
    tel_no = models.CharField(null=True, max_length=100)
    fax_no = models.CharField(null=True, max_length=100)
    email = models.CharField(null=True, max_length=100)
    homepage_url = models.CharField(null=True, max_length=2000)
    inst_desc = models.CharField(null=True, max_length=2000)
    establishment_dt = models.DateField(null=True)
    inst_operation_status_cd = models.CharField(null=True, max_length=10)
    longitude_val = models.CharField(null=True, max_length=100)
    latitude_val = models.CharField(null=True, max_length=100)
    info_mng_inst_id = models.CharField(null=True, max_length=10)
    info_inp_inst_id = models.CharField(null=True, max_length=10)
    tag = models.CharField(null=True, max_length=10)
    loc_leic_appnt_yn = models.CharField(max_length=1)
    life_study_center_appnt_cd = models.CharField(null=True, max_length=10)
    incumbenttrain_inst_yn = models.CharField(max_length=1)
    cb_inst_yn = models.CharField(max_length=1)
    lfllr_inst_yn = models.CharField(max_length=1)
    psdc_appnt_inst_yn = models.CharField(max_length=1)
    basic_lit_edu_yn = models.CharField(max_length=1)
    achv_sppl_edu_yn = models.CharField(max_length=1)
    job_ability_edu_yn = models.CharField(max_length=1)
    culture_art_edu_yn = models.CharField(max_length=1)
    human_rfnmnt_edu_yn = models.CharField(max_length=1)
    citizen_join_edu_yn = models.CharField(max_length=1)
    inst_class1_cd = models.CharField(null=True, max_length=10)
    inst_class2_cd = models.CharField(null=True, max_length=10)
    inst_class3_cd = models.CharField(null=True, max_length=10)
    reg_user_id = models.CharField(null=True, max_length=30)
    reg_dt = models.DateField(null=True)
    upd_user_id = models.CharField(null=True, max_length=30)
    upd_dt = models.DateField(null=True)
    #del_yn = models.CharField(max_length=1)
    page_cnt = models.CharField(null=True, max_length=100)
    page_no = models.CharField(null=True, max_length=100)
    total_cnt = models.CharField(null=True, max_length=100)
    task_id = models.CharField(null=True, max_length=100)
    class Meta:
        db_table = "CRAWL_INST_INFO"