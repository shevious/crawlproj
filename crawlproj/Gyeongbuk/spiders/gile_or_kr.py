from __future__ import absolute_import

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.starturls import FeedGenerator, FragmentGenerator
from ..utils.processors import Item, Field, Text, Number, Price, Date, Url, Image, Regex
from ..items import PortiaItem, CourseInfoItem

import pytz, datetime, re

class GileOrKr(BasePortiaSpider):
    name = "www.gile.or.kr"
    allowed_domains = ['www.gile.or.kr']
    start_urls = [
        #'http://www.gile.or.kr/web/lecture/view.do?mId=72&page=1&organIdx=2019111800000001&lecIdx=2019120900000003']
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&page=1']
    rules = [
        Rule(
            LinkExtractor(
                #allow=('www.gile.or.kr\\/web\\/lecture\\/list.do\\?mId=72&page=\d'),
                allow=('www.gile.or.kr\\/web\\/lecture\\/list.do\\?mId=72&page=1$'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        )
    ]
    items = [
        [
            Item(
                CourseInfoItem,
                None,
                '.viewTypeA',
                [
                    Field(
                        'course_nm',
                        'thead > tr > th *::text',
                        []),
                    Field(
                        'org',
                        'tr:nth-child(1) > td *::text, tbody > tr:nth-child(1) > td *::text',
                        []),
                    Field(
                        'course_period',
                        'tr:nth-child(2) > td:nth-child(2) *::text, tbody > tr:nth-child(2) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'receive_period',
                        'tr:nth-child(2) > td:nth-child(4) *::text, tbody > tr:nth-child(2) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'teacher_pernm',
                        'tr:nth-child(3) > td:nth-child(2) *::text, tbody > tr:nth-child(3) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'enroll_amt',
                        'tr:nth-child(3) > td:nth-child(4) *::text, tbody > tr:nth-child(3) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'edu_method_cd',
                        'tr:nth-child(4) > td:nth-child(2) *::text, tbody > tr:nth-child(4) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'edu_target_cd',
                        'tr:nth-child(4) > td:nth-child(4) *::text, tbody > tr:nth-child(4) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'edu_cycle_content',
                        'tr:nth-child(5) > td:nth-child(2) *::text, tbody > tr:nth-child(5) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'edu_quota_cnt',
                        'tr:nth-child(5) > td:nth-child(4) *::text, tbody > tr:nth-child(5) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'edu_location_desc',
                        'tr:nth-child(6) > td:nth-child(2) *::text, tbody > tr:nth-child(6) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'inquiry_tel_no',
                        'tr:nth-child(6) > td:nth-child(4) *::text, tbody > tr:nth-child(6) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'enroll_appl_method_cd',
                        'tr:nth-child(7) > td:nth-child(2) *::text, tbody > tr:nth-child(7) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'enroll_status',
                        'tr:nth-child(7) > td:nth-child(4) *::text, tbody > tr:nth-child(7) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'job_ability_course_yn',
                        'tr:nth-child(8) > td:nth-child(2) *::text, tbody > tr:nth-child(8) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'cb_eval_accept_yn',
                        'tr:nth-child(8) > td:nth-child(4) *::text, tbody > tr:nth-child(8) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'all_eval_accept_inst',
                        'tr:nth-child(9) > td:nth-child(2) *::text, tbody > tr:nth-child(9) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'lang_cd',
                        'tr:nth-child(10) > td:nth-child(2) *::text, tbody > tr:nth-child(10) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'vsl_handicap_supp_yn',
                        'tr:nth-child(10) > td:nth-child(4) *::text, tbody > tr:nth-child(10) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'hrg_handicap_supp_yn',
                        'tr:nth-child(11) > td:nth-child(2) *::text, tbody > tr:nth-child(11) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'link_url',
                        'tr:nth-child(11) > .link > a::attr(href), tbody > tr:nth-child(11) > .link > a::attr(href)',
                        []),
                    Field(
                        'course_desc',
                        'tr:nth-child(12) > .contents *::text, tbody > tr:nth-child(12) > .contents *::text',
                        [])])]]


    def parse_item(self, response):

        links = response.xpath("//div/span[@class='tit']/a/@href")

        for link in links:
            href = link.extract()
            #test = link.re("'(.+?)'")
            #테스트용 if문 (1페이지만)
            #if (href.find("page=1&")) > int(0) :
            url = "http://www.gile.or.kr/web/lecture/" + href
            yield Request(url, self.parse_item)

        for sample in self.items:
            items = []
            itemUrl = response.url
            if itemUrl.find("view.do") > 0:  # 상세URL만 읽음
                try:
                    for definition in sample:
                        items.extend(
                            [i for i in self.load_item(definition, response)]
                        )
                except RequiredFieldMissing as exc:
                    self.logger.warning(str(exc))
                if items:
                    for item in items:
                        # item['url'] = response.url
                        idxs = re.search(r"organIdx=([^&]*)&lecIdx=([^&]*)", itemUrl)
                        item['url'] = itemUrl  # URL
                        # item['inst_id'] = idxs.group(1) + '_' + idxs.group(2)  # 기관ID
                        item['course_id'] = idxs.group(1) + '_' + idxs.group(2)  # 강좌ID
                        item['enroll_amt'] = (re.sub(r'\([^)]*\)', '', item['enroll_amt'])).strip()   # 수강료
                        course_period = re.match('(\d{4}-\d{2}-\d{2})~(\d{4}-\d{2}-\d{2})',
                                                 re.sub('[ ]', '', item['course_period']))  # 강좌기간
                        receive_period = re.match('(\d{4}-\d{2}-\d{2})~(\d{4}-\d{2}-\d{2})',
                                                   re.sub('[ ]', '', item['receive_period']))  # 접수기간

                        if course_period != None:   # 강좌시작일, 강좌종료일
                            item['course_start_dt'] = course_period.group(1)
                            item['course_end_dt'] = course_period.group(2)
                        if receive_period != None: # 접수시작일, 접수종료일
                            item['receive_start_dt'] = receive_period.group(1)
                            item['receive_end_dt'] = receive_period.group(2)
                        if item['all_eval_accept_inst'] == '인정기관':  # 평생학습계좌제평가인정여부
                            item['all_eval_accept_yn'] = 'Y'
                        else:
                            item['all_eval_accept_yn'] = 'N'
                        if item['cb_eval_accept_yn'] == '지원':  # 학점은행제평가인정여부
                            item['cb_eval_accept_yn'] = 'Y'
                        else:
                            item['cb_eval_accept_yn'] = 'N'
                        if item['job_ability_course_yn'] == '훈련기관':  # 직업능력강좌여부
                            item['job_ability_course_yn'] = 'Y'
                        else:
                            item['job_ability_course_yn'] = 'N'
                        if item['vsl_handicap_supp_yn'] == '지원':  # 시각장애지원여부
                            item['vsl_handicap_supp_yn'] = 'Y'
                        else:
                            item['vsl_handicap_supp_yn'] = 'N'
                        if item['hrg_handicap_supp_yn'] == '지원':  # 청각장애지원여부
                            item['hrg_handicap_supp_yn'] = 'Y'
                        else:
                            item['hrg_handicap_supp_yn'] = 'N'

                        dt = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))
                        item['date'] = "%s:%.3f%s" % (
                            dt.strftime('%Y-%m-%dT%H:%M'),
                            float("%.3f" % (dt.second + dt.microsecond / 1e6)),
                            dt.strftime('%z')
                        )
                        yield item
                    break