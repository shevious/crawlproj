from __future__ import absolute_import

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from scrapy.spiders import Rule
from scrapy.utils.response import get_base_url

from ..utils.spiders import BasePortiaSpider
from ..utils.starturls import FeedGenerator, FragmentGenerator
from ..utils.processors import Item, Field, Text, Number, Price, Date, Url, Image, Regex
from ..items import PortiaItem, InstItemItem

import pytz, datetime, re

class UillOrKr(BasePortiaSpider):
    name = "www.uill.or.kr.inst"
    allowed_domains = ['www.uill.or.kr']
    start_urls = [
        'http://www.uill.or.kr/UR/info/organ/list.do?rbsIdx=35&page=1']
    rules = [
        Rule(
            LinkExtractor(
                allow=('www\\.uill\\.or\\.kr\\/UR\\/info\\/organ\\/list.do\\?rbsIdx=35&page=\d'),
                #allow=('www\\.uill\\.or\\.kr\\/UR\\/info\\/organ\\/list.do\\?rbsIdx=35&page=1$'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        )
    ]
    items = [
        [
            Item(
                InstItemItem,
                None,
                '#bbs_box03_list',
                [
                    Field(
                        'inst_nm',
                        'h3 *::text',
                        []),
                    Field(
                        'inst_ceo_pernm',
                        'div:nth-child(4) > .cle > .table02 > table > tr:nth-child(1) > td:nth-child(2) *::text, div:nth-child(4) > .cle > .table02 > table > tbody > tr:nth-child(1) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'inst_set_up_main_agent',
                        'div:nth-child(4) > .cle > .table02 > table > tr:nth-child(1) > td:nth-child(4) *::text, div:nth-child(4) > .cle > .table02 > table > tbody > tr:nth-child(1) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'establishment_dt',
                        'div:nth-child(4) > .cle > .table02 > table > tr:nth-child(2) > td:nth-child(2) *::text, div:nth-child(4) > .cle > .table02 > table > tbody > tr:nth-child(2) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'inst_operation_status_cd',
                        'div:nth-child(4) > .cle > .table02 > table > tr:nth-child(2) > td:nth-child(4) *::text, div:nth-child(4) > .cle > .table02 > table > tbody > tr:nth-child(2) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'tel_no',
                        'div:nth-child(4) > .cle > .table02 > table > tr:nth-child(3) > td:nth-child(2) *::text, div:nth-child(4) > .cle > .table02 > table > tbody > tr:nth-child(3) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'fax_no',
                        'div:nth-child(4) > .cle > .table02 > table > tr:nth-child(3) > td:nth-child(4) *::text, div:nth-child(4) > .cle > .table02 > table > tbody > tr:nth-child(3) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'manager_pernm',
                        'div:nth-child(4) > .cle > .table02 > table > tr:nth-child(4) > td:nth-child(2) *::text, div:nth-child(4) > .cle > .table02 > table > tbody > tr:nth-child(4) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'homepage_url',
                        'div:nth-child(4) > .cle > .table02 > table > tr:nth-child(4) > .email *::text, div:nth-child(4) > .cle > .table02 > table > tbody > tr:nth-child(4) > .email *::text',
                        []),
                    Field(
                        'email',
                        'div:nth-child(4) > .cle > .table02 > table > tr:nth-child(5) > .email *::text, div:nth-child(4) > .cle > .table02 > table > tbody > tr:nth-child(5) > .email *::text',
                        []),
                    Field(
                        'inst_operation_form_cd',
                        'div:nth-child(4) > .cle > .table02 > table > tr:nth-child(5) > .num *::text, div:nth-child(4) > .cle > .table02 > table > tbody > tr:nth-child(5) > .num *::text',
                        []),
                    Field(
                        'address',
                        'div:nth-child(4) > .cle > .table02 > table > tr:nth-child(6) > td *::text, div:nth-child(4) > .cle > .table02 > table > tbody > tr:nth-child(6) > td *::text',
                        []),
                    Field(
                        'inst_desc',
                        'div:nth-child(4) > .cle > .table02 > table > tr:nth-child(7) > td *::text, div:nth-child(4) > .cle > .table02 > table > tbody > tr:nth-child(7) > td *::text',
                        [])])]]

    def parse_item(self, response):
        links = response.xpath("//*[@class ='table01']/table/tbody/tr/td[2]/a/@href")

        for link in links:
            arg = link.extract()
            url = "http://www.uill.or.kr" + arg
            yield Request(url, self.parse_item)

        for sample in self.items:
            items = []

            itemUrl = response.url
            if itemUrl.find("info.do") > 0:     #상세URL만 읽음
                try:
                    for definition in sample:
                        items.extend(
                            [i for i in self.load_item(definition, response)]
                        )
                except RequiredFieldMissing as exc:
                    self.logger.warning(str(exc))
                if items:
                    for item in items:
                        #item['url'] = response.url
                        organidx = re.search(r"organIdx=([^&]*)", itemUrl)
                        item['url'] = itemUrl       #URL
                        item['inst_id'] = organidx.group(1)     #기관ID
                        item['inst_id_org'] = organidx.group(1)  # 기관ID(원형)

                        address = re.search(r"\((.*?)\).(.*)", item['address'])

                        if address == None:
                            item['zipcode'] = None
                            item['addr1'] = item['address']
                        else:
                            item['zipcode'] = address.group(1)
                            item['addr1'] = address.group(2)

                        try:    # 기관소개
                            item['inst_desc'] = re.sub('[\xa0]', ' ', item['inst_desc'])
                        except KeyError:
                            item['inst_desc'] = None

                        try:    # 기관설립주체
                            if item['inst_set_up_main_agent'] == '법인':
                                item['inst_set_up_main_agent_cd'] = '01'
                            elif item['inst_set_up_main_agent'] == '개인':
                                item['inst_set_up_main_agent_cd'] = '02'
                            elif item['inst_set_up_main_agent'] == '국가/지자체':
                                item['inst_set_up_main_agent_cd'] = '03'
                            elif item['inst_set_up_main_agent'] == '기타':
                                item['inst_set_up_main_agent_cd'] = '04'
                            elif item['inst_set_up_main_agent'].strip() == '':
                                item['inst_set_up_main_agent_cd'] = None
                            else:   # 그 외
                                item['inst_set_up_main_agent_cd'] = '05'
                        except KeyError:
                            item['inst_set_up_main_agent_cd'] = None

                        try:    # 기관운영상태
                            if item['inst_operation_status_cd'] == '운영중':
                                item['inst_operation_status_cd'] = '01'
                            elif item['inst_operation_status_cd'] == '연락두절':
                                item['inst_operation_status_cd'] = '02'
                            elif item['inst_operation_status_cd'] == '폐원':
                                item['inst_operation_status_cd'] = '03'
                            elif item['inst_operation_status_cd'].strip() == '':
                               item['inst_operation_status_cd'] = None
                            else:   # 그 외
                                item['inst_operation_status_cd'] = '04'
                        except KeyError:
                            item['inst_operation_status_cd'] = None

                        try:    # 운영형태
                            if item['inst_operation_form_cd'] == '직영':
                                item['inst_operation_form_cd'] = '01'
                            elif item['inst_operation_form'] == '위탁':
                                item['inst_operation_form_cd'] = '02'
                            elif item['inst_operation_form'] == '병행':
                                item['inst_operation_form_cd'] = '03'
                            elif item['inst_operation_form_cd'].strip() == '':
                                item['inst_operation_form_cd'] = None
                            else:   # 그 외
                                item['inst_operation_form_cd'] = '04'
                        except KeyError:
                            item['inst_operation_form_cd'] = None

                        # 초기값
                        keyarray = ['inst_ceo_pernm', 'manager_pernm', 'tel_no', 'fax_no', 'email', 'homepage_url',
                                    'establishment_dt']
                        for keyitem in keyarray:
                            try:
                                item[keyitem] = item[keyitem].strip()
                            except KeyError:
                                item[keyitem] = None

                        dt = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))
                        item['date'] =  "%s:%.3f%s" % (
                            dt.strftime('%Y-%m-%dT%H:%M'),
                            float("%.3f" % (dt.second + dt.microsecond / 1e6)),
                            dt.strftime('%z')
                        )
                        yield item
                    break