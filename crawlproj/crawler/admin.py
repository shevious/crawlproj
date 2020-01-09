from django.contrib import admin
from .models import Con_log, Inst_info, Course_info

#admin.site.register(Con_log)

class Con_log_admin(admin.ModelAdmin):
    list_display = ['con_log_id', 'con_id', 'con_tm', 'con_kind_cd', 'con_status_cd', 'log_desc']

class Inst_info_admin(admin.ModelAdmin):
    list_display = ['inst_id', 'con_id', 'sido_cd', 'sigungu_cd', 'inst_nm',
        'inst_ceo_pernm',
        'zipcode',
        'addr1',
        'inst_desc',
    ]
    list_filter = ['sido_cd', 'sigungu_cd']

class Course_info_admin(admin.ModelAdmin):
    list_display = ['course_id', 'sido_cd', 'sigungu_cd', 'course_nm',
        'edu_location_desc',
        'tag',
        'course_desc',
    ]
    list_filter = ['sido_cd', 'sigungu_cd']

admin.site.register(Con_log, Con_log_admin)
admin.site.register(Inst_info, Inst_info_admin)
admin.site.register(Course_info, Course_info_admin)
