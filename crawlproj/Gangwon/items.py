from __future__ import absolute_import

import scrapy
from collections import defaultdict
from scrapy.loader.processors import Join, MapCompose, Identity
from w3lib.html import remove_tags
from .utils.processors import Text, Number, Price, Date, Url, Image


class PortiaItem(scrapy.Item):
    fields = defaultdict(
        lambda: scrapy.Field(
            input_processor=Identity(),
            output_processor=Identity()
        )
    )

    def __setitem__(self, key, value):
        self._values[key] = value

    def __repr__(self):
        data = str(self)
        if not data:
            return '%s' % self.__class__.__name__
        return '%s(%s)' % (self.__class__.__name__, data)

    def __str__(self):
        if not self._values:
            return ''
        string = super(PortiaItem, self).__repr__()
        return string


class ItemnameItem(PortiaItem):
    org = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    teacher_pernm = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    course_period = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    course_nm = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    register_period = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    enroll_amt = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    course_desc = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    job_ability_course = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    edu_cycle_content = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    vsl_handicap_supp = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    cb_eval_accept = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    edu_status = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    inquiry_tel_no = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    edu_quota_cnt = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    hrg_handicap_supp = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    all_eval_accept = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    lang_cd = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    enroll_appl_method_cd = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    edu_method_cd = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    edu_location_desc = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    enroll_status = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )