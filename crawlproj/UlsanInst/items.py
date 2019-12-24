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


class InstItemItem(PortiaItem):
    inst_operation_form_cd = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    homepage_url = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    inst_set_up_main_agent = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    AD = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    inst_operation_status_cd = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    email = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    manager_pernm = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    address = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    fax_no = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    tel_no = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    establishment_dt = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    inst_desc = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    inst_ceo_pernm = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
    inst_nm = scrapy.Field(
        input_processor=Text(),
        output_processor=Join(),
    )
