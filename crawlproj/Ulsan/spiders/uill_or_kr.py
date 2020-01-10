from __future__ import absolute_import

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.starturls import FeedGenerator, FragmentGenerator
from ..utils.processors import Item, Field, Text, Number, Price, Date, Url, Image, Regex
from ..items import Dfd_42Ed_8AabItem, PortiaItem

import pytz, datetime
import re

class UillOrKr(BasePortiaSpider):
    name = "www.uill.or.kr"
    allowed_domains = ['www.uill.or.kr']
    start_urls = [
        #'http://www.uill.or.kr/UR/info/lecture/view.do?rbsIdx=34&page=1&organIdx=3175&idx=EX18651'
        'http://www.uill.or.kr/UR/info/lecture/list.do?rbsIdx=34&page=1'
    ]
    rules = [
        Rule(
            LinkExtractor(
                allow=('www\\.uill\\.or\\.kr\\/UR\\/info\\/lecture\\/list\\.do\\?rbsIdx=34&page=\d'),
                #allow=('www\\.uill\\.or\\.kr\\/UR\\/info\\/lecture\\/view.do\\?rbsIdx=34\\&page=1\\&organIdx=3175\\&idx=EX18651'),
                #allow=('www\\.uill\\.or\\.kr\\/UR\\/info\\/lecture\\/list\\.do\\?rbsIdx=34&page=1$'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        ),
        Rule(
            LinkExtractor(
                #allow=('(www\\.uill\\.or\\.kr\\/UR\\/info\\/lecture\\/list\\.do\\?rbsIdx=34&page=2$|view\.do)'),
                allow=('www\\.uill\\.or\\.kr\\/UR\\/info\\/lecture\\/view.do'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        ),
    ]
    items = [
        [
            Item(
                Dfd_42Ed_8AabItem,
                None,
                '#bbs_box02_view',
                [
                    Field(
                        'course_nm',
                        'h2 *::text',
                        []),
                    Field(
                        'teacher_pernm',
                        '.cle > table > tr:nth-child(5) > td:nth-child(2) *::text, .cle > table > tbody > tr:nth-child(3) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'course_period',
                        '.cle > table > tr:nth-child(4) > td:nth-child(2) *::text, .cle > table > tbody > tr:nth-child(2) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'org',
                        '.cle > table > tr:nth-child(3) > td *::text, .cle > table > tbody > tr:nth-child(1) > td *::text',
                        []),
                    Field(
                        'edu_method_cd',
                        '.cle > table > tr:nth-child(6) > td:nth-child(2) *::text, .cle > table > tbody > tr:nth-child(4) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'enroll_amt',
                        '.cle > table > tr:nth-child(5) > td:nth-child(4) *::text, .cle > table > tbody > tr:nth-child(3) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'receive_period',
                        '.cle > table > tr:nth-child(4) > td:nth-child(4) *::text, .cle > table > tbody > tr:nth-child(2) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'edu_target_cd',
                        '.cle > table > tr:nth-child(6) > td:nth-child(4) *::text, .cle > table > tbody > tr:nth-child(4) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'edu_cycle_content',
                        '.cle > table > tr:nth-child(7) > td:nth-child(2) *::text, .cle > table > tbody > tr:nth-child(5) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'edu_quota_cnt',
                        '.cle > table > tr:nth-child(7) > td:nth-child(4) *::text, .cle > table > tbody > tr:nth-child(5) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'edu_location_desc',
                        '.cle > table > tr:nth-child(8) > td:nth-child(2) *::text, .cle > table > tbody > tr:nth-child(6) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'inquiry_tel_no',
                        '.cle > table > tr:nth-child(8) > td:nth-child(4) *::text, .cle > table > tbody > tr:nth-child(6) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'enroll_appl_method_cd',
                        '.cle > table > tr:nth-child(9) > td:nth-child(2) *::text, .cle > table > tbody > tr:nth-child(7) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'link_url',
                        '.cle > table > tr:nth-child(10) > td *::text, .cle > table > tbody > tr:nth-child(8) > td *::text',
                        [])
                ]
            )
        ]
    ]

    def parse_item(self, response):
        links = response.xpath("//a/@onclick[contains(.,'fn_applCheck2')]")
        for link in links:
            arg = link.re("'(.+?)'")
            url = "http://www.uill.or.kr/UR/info/lecture/" + arg[0]
            yield Request(url, self.parse_item)

        for sample in self.items:
            items = []
            try:
                for definition in sample:
                    items.extend(
                        [i for i in self.load_item(definition, response)]
                    )
            except RequiredFieldMissing as exc:
                self.logger.warning(str(exc))
            if items:
                for item in items:
                    item['url'] = response.url
                    dt = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))
                    item['date'] =  "%s:%.3f%s" % (
                        dt.strftime('%Y-%m-%dT%H:%M'),
                        float("%.3f" % (dt.second + dt.microsecond / 1e6)),
                        dt.strftime('%z')
                    )
                    match = re.search(r'(?<=organIdx=)([^&]*)&idx=([^&]*)', response.url) 
                    item['course_id'] = match.group(1) + '_' + match.group(2)
                    item['course_id_org'] = match.group(1) + '_' + match.group(2)  # 강좌ID

                    course_period = re.match(r'(\d{4}-\d{2}-\d{2})~(\d{4}-\d{2}-\d{2})',
                                             re.sub('[ \xa0]', '', item['course_period']))  # 강좌기간
                    receive_period = re.match(r'(\d{4}-\d{2}-\d{2})~(\d{4}-\d{2}-\d{2})',
                                              re.sub('[ \xa0]', '', item['receive_period']))  # 접수기간
                    if course_period != None:  # 강좌시작일, 강좌종료일
                        item['course_start_dt'] = course_period.group(1)
                        item['course_end_dt'] = course_period.group(2)
                    if receive_period != None:  # 접수시작일, 접수종료일
                        item['receive_start_dt'] = receive_period.group(1)
                        item['receive_end_dt'] = receive_period.group(2)

                    # 초기값
                    keyarray = ['org', 'teacher_pernm', 'enroll_amt', 'edu_method_cd', 'edu_cycle_content'
                        , 'course_start_dt', 'course_end_dt', 'receive_start_dt', 'receive_end_dt'
                        , 'edu_location_desc', 'inquiry_tel_no', 'edu_quota_cnt', 'lang_cd', 'job_ability_course_yn'
                        ,'cb_eval_accept_yn', 'all_eval_accept_yn', 'vsl_handicap_supp_yn', 'hrg_handicap_supp_yn'
                        , 'edu_target_cd', 'course_desc', 'link_url', 'enroll_appl_method_cd']
                    
                    for keyitem in keyarray:
                        try:
                            item[keyitem] = item[keyitem].strip()
                            if keyitem == 'edu_method_cd':
                                item[keyitem] = (re.sub(r'\([^)]*\)', '', item[keyitem])).strip()   # 교육방법
                            elif keyitem == 'enroll_appl_method_cd':    # 접수방법
                                item[keyitem] = item[keyitem].replace('방문신청', 'visit')
                                item[keyitem] = item[keyitem].replace('온라인신청', 'online')
                                item[keyitem] = (item[keyitem].replace('전화신청', 'call')).replace('/', '')
                        except KeyError:
                            if keyitem == 'edu_location_desc':
                                item[keyitem] = ''
                            else:
                                item[keyitem] = None
                    yield item
                break

