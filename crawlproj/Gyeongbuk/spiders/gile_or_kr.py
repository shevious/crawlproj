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
import hashlib

class GileOrKr(BasePortiaSpider):
    name = "www.gile.or.kr"
    allowed_domains = ['www.gile.or.kr']
    start_urls = [
        #'http://www.gile.or.kr/web/lecture/view.do?mId=72&page=1&organIdx=2019111800000001&lecIdx=2019120900000003']
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&page=1'
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4711&page=1',
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4713&page=1',
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4715&page=1',
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4717&page=1',
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4719&page=1',
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4721&page=1',
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4723&page=1',
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4725&page=1', #상주
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4728&page=1', #문경
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4729&page=1', #경산
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4772&page=1', #군위
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4773&page=1', #의성
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4775&page=1', #청송
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4776&page=1', #영양
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4776&page=1', #영양
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4777&page=1', #영덕
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4782&page=1', #청도
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4783&page=1', #고령
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4784&page=1', #성주
        #'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4785&page=1', #칠곡
    ]
    rules = [
        Rule(
            LinkExtractor(
                allow=('www.gile.or.kr\\/web\\/lecture\\/list.do\\?mId=72&page=\\d+$',
                       'www.gile.or.kr\\/web\\/lecture\\/list.do\\?mId=72&is_ord_local_cd=\\d+&page=\\d+$'),
                #allow=('www.gile.or.kr\\/web\\/lecture\\/list.do\\?mId=72&is_ord_local_cd=\\d+$'),
                #allow=('www.gile.or.kr\\/web\\/lecture\\/list.do\\?mId=72&page=\\d+'),
                #allow=('www.gile.or.kr\\/web\\/lecture\\/list.do\\?mId=72&page=1$'),
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
                        'job_ability_course_yn',
                        'tr:nth-child(8) > td:nth-child(2) *::text, tbody > tr:nth-child(8) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'cb_eval_accept_yn',
                        'tr:nth-child(8) > td:nth-child(4) *::text, tbody > tr:nth-child(8) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'all_eval_accept_yn',
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


    def parse_item(self, response, *args, **kw):

        links = response.xpath("//div/span[@class='tit']/a/@href")

        for link in links:
            href = link.extract()
            #test = link.re("'(.+?)'")
            #테스트용 if문 (1페이지만)
            #if (href.find("page=1&")) > int(0) :
            #print("href : ", href)
            url = "http://www.gile.or.kr/web/lecture/" + href
            gugun = re.search(r'(?<=is_ord_local_cd=)([^&]*)&', response.url)
            if gugun == None:
                yield Request(url, self.parse_item)
            else:
                location = gugun.group(1)
                yield Request(url, self.parse_item, cb_kwargs={'location': location})

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
                    header = 'GB'
                    for item in items:
                        if 'location' in kw.keys():
                            item['sigungu_cd'] = kw['location']
                        # item['url'] = response.url
                        idxs = re.search(r"organIdx=([^&]*)&lecIdx=([^&]*)", itemUrl)
                        item['url'] = itemUrl  # URL
                        # item['inst_id'] = idxs.group(1) + '_' + idxs.group(2)  # 기관ID
                        organIdx = idxs.group(1)
                        lecIdx = idxs.group(2)
                        hash = hashlib.sha1(f'{organIdx}{lecIdx}'.encode('UTF-8')).hexdigest()
                        item['course_id'] = hash[:30]
                        item['course_id_org'] = header + organIdx + "_" + lecIdx    # 강좌ID

                        #item['course_id'] = idxs.group(2)  # 강좌ID
                        item['enroll_amt'] = (re.sub(r'\(.*\)', '', item['enroll_amt'])).strip()   # 수강료
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
                        if item['all_eval_accept_yn'] == '인정기관':  # 평생학습계좌제평가인정여부
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

                        # 초기값
                        keyarray = ['org', 'teacher_pernm', 'enroll_amt', 'edu_method_cd', 'edu_cycle_content'
                                    , 'course_start_dt', 'course_end_dt', 'receive_start_dt', 'receive_end_dt'
                                    , 'edu_location_desc', 'inquiry_tel_no', 'edu_quota_cnt', 'lang_cd'
                                    , 'edu_target_cd', 'course_desc', 'link_url', 'enroll_appl_method_cd']
                        for keyitem in keyarray:
                            try:
                                item[keyitem] = item[keyitem].strip()
                                if keyitem == 'lang_cd':
                                    item[keyitem] = item[keyitem].lower()
                                elif keyitem == 'edu_method_cd':
                                    item[keyitem] = (item[keyitem].replace('Corrente', '')).strip()
                                elif keyitem == 'enroll_appl_method_cd':
                                    item[keyitem] = item[keyitem].replace('방문접수', 'visit')
                                    item[keyitem] = item[keyitem].replace('온라인접수', 'online')
                                    item[keyitem] = (item[keyitem].replace('전화접수', 'call')).replace('/', '')
                            except KeyError:
                                item[keyitem] = None
                        if item['link_url'] == None:
                            item['link_url'] = itemUrl

                        dt = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))
                        item['date'] = "%s:%.3f%s" % (
                            dt.strftime('%Y-%m-%dT%H:%M'),
                            float("%.3f" % (dt.second + dt.microsecond / 1e6)),
                            dt.strftime('%z')
                        )
                        yield item
                    break

class GileOrKr2(GileOrKr):
    name = "www.gile.or.kr2"
    start_urls = [
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4711&page=1', #포항
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4713&page=1',
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4715&page=1',
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4717&page=1',
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4719&page=1',
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4721&page=1',
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4723&page=1',
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4725&page=1', #상주
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4728&page=1', #문경
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4729&page=1', #경산
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4772&page=1', #군위
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4773&page=1', #의성
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4775&page=1', #청송
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4776&page=1', #영양
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4776&page=1', #영양
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4777&page=1', #영덕
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4782&page=1', #청도
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4783&page=1', #고령
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4784&page=1', #성주
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4785&page=1', #칠곡
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4790&page=1', #예천
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4793&page=1', #봉화
        'http://www.gile.or.kr/web/lecture/list.do?mId=72&is_ord_local_cd=4794&page=1', #울릉
    ]
