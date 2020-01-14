from django.contrib import admin
from .models import Con_log, Inst_info, Course_info
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

class Con_log_admin(admin.ModelAdmin):
    list_display = ['con_log_id', 'con_id', 'con_tm', 'con_kind_cd', 'con_status_cd', 'log_desc']

class Inst_info_admin(admin.ModelAdmin):
    list_display = ['inst_id', 'con_id', 'sido_cd', 'sigungu_cd', 'inst_nm',
        'inst_ceo_pernm',
        'zipcode',
        'addr1',
        'inst_desc',
        'upd_dt',
    ]
    list_filter = ['sido_cd', 'sigungu_cd']
    readonly_fields = ['reg_dt', 'upd_dt']

class Course_info_admin(admin.ModelAdmin):
    list_display = [ 'course_nm',
        'edu_location_desc',
        #'sigungu_cd',
        'tag',
        'course_desc',
        'inquiry_tel_no',
        'teacher_pernm',
        'enroll_amt',
        'edu_target_cd',
        'link_url',
        #'upd_dt',
    ]
    list_filter = [('upd_dt', DateRangeFilter), 'sido_cd', 'sigungu_cd',]
    readonly_fields = ['reg_dt', 'upd_dt']

admin.site.register(Con_log, Con_log_admin)
admin.site.register(Inst_info, Inst_info_admin)
admin.site.register(Course_info, Course_info_admin)
