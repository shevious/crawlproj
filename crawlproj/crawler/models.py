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
    class Meta:
        db_table = "CRAWL_COURSE_INFO"
