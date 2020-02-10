from __future__ import absolute_import

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.starturls import FeedGenerator, FragmentGenerator
from ..utils.processors import Item, Field, Text, Number, Price, Date, Url, Image, Regex
from ..items import PortiaItem, ItemnameItem

import pytz, datetime, re
from scrapy.selector import Selector

class ERoomOrKr(BasePortiaSpider):
    name = "www.e-room.or.kr"
    allowed_domains = ['www.e-room.or.kr']
    start_urls = [
        'https://www.e-room.or.kr/gw/portal/org_lecture_info?mode=list&leccode=&page_no=1&selectRegion=&gubun=&studyKind=&searchKeyWord=&searchFromDate=&searchEndDate='
        #'https://www.e-room.or.kr/gw/portal/org_lecture_info?mode=read&leccode=3444&page_no=1&selectRegion=&gubun=&studyKind=&searchKeyWord=&searchFromDate=&searchEndDate=' # enroll_amt == None case
        #'https://www.e-room.or.kr/gw/portal/org_lecture_info?mode=read&leccode=4647&page_no=1&selectRegion=&gubun=&studyKind=&searchKeyWord=&searchFromDate=&searchEndDate='
        #'https://www.e-room.or.kr/gw/portal/org_lecture_info?mode=read&leccode=4633&page_no=1&selectRegion=&gubun=&studyKind=&searchKeyWord=&searchFromDate=&searchEndDate='
        #'https://www.e-room.or.kr/gw/portal/org_lecture_info?mode=read&leccode=4647&page_no=1&selectRegion=&gubun=&studyKind=&searchKeyWord=&searchFromDate=&searchEndDate='
        #'https://www.e-room.or.kr/gw/portal/org_lecture_info?mode=read&leccode=3047&page_no=1&selectRegion=&gubun=&studyKind=&searchKeyWord=&searchFromDate=&searchEndDate='
        #'https://www.e-room.or.kr/gw/portal/org_lecture_info?mode=read&leccode=2000&page_no=1&selectRegion=&gubun=&studyKind=&searchKeyWord=&searchFromDate=&searchEndDate'
        #'https://www.e-room.or.kr/gw/portal/org_lecture_info?mode=read&leccode=970&page_no=1&selectRegion=&gubun=&studyKind=&searchKeyWord=&searchFromDate=&searchEndDate' # 'http://' as url
        #'https://www.e-room.or.kr/gw/portal/org_lecture_info?mode=read&leccode=999&page_no=1&selectRegion=&gubun=&studyKind=&searchKeyWord=&searchFromDate=&searchEndDate' # 'http://' as url
        #'https://www.e-room.or.kr/gw/portal/org_lecture_info?mode=list&leccode=&page_no=2&selectRegion=&gubun=&studyKind=&searchKeyWord=&searchFromDate=&searchEndDate='
    ]
    rules = [
        Rule(
            LinkExtractor(
                allow=('www.e-room.or.kr\\/gw\\/portal\\/org_lecture_info\\?mode=list'),
                #allow=('www.e-room.or.kr\\/gw\\/portal\\/org_lecture_info\\?mode=read'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        )
    ]
    items = [
        [
            Item(
                ItemnameItem,
                None,
                '.content',
                [
                    Field(
                        'course_nm',
                        'h3 *::text',
                        []),
                    Field(
                        'org',
                        '.input_01 > tr:nth-child(1) > td *::text, .input_01 > tbody > tr:nth-child(1) > td *::text',
                        []),
                    Field(
                        'course_period',
                        '.input_01 > tr:nth-child(2) > td:nth-child(2) *::text, .input_01 > tbody > tr:nth-child(2) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'register_period',
                        '.input_01 > tr:nth-child(2) > td:nth-child(4) *::text, .input_01 > tbody > tr:nth-child(2) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'teacher_pernm',
                        '.input_01 > tr:nth-child(3) > td:nth-child(2) *::text, .input_01 > tbody > tr:nth-child(3) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'enroll_amt',
                        '.input_01 > tr:nth-child(3) > td:nth-child(4) *::text, .input_01 > tbody > tr:nth-child(3) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'edu_method_cd',
                        '.input_01 > tr:nth-child(4) > td:nth-child(2) *::text, .input_01 > tbody > tr:nth-child(4) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'edu_cycle_content',
                        '.input_01 > tr:nth-child(4) > td:nth-child(4) *::text, .input_01 > tbody > tr:nth-child(4) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'edu_location_desc',
                        '.input_01 > tr:nth-child(5) > td:nth-child(2) *::text, .input_01 > tbody > tr:nth-child(5) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'inquiry_tel_no',
                        '.input_01 > tr:nth-child(5) > td:nth-child(4) *::text, .input_01 > tbody > tr:nth-child(5) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'edu_quota_cnt',
                        '.input_01 > tr:nth-child(6) > td:nth-child(2) *::text, .input_01 > tbody > tr:nth-child(6) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'enroll_status',
                        '.input_01 > tr:nth-child(6) > td:nth-child(4) > .icon_img::attr(alt), .input_01 > tbody > tr:nth-child(6) > td:nth-child(4) > .icon_img::attr(alt)',
                        []),
                    Field(
                        'enroll_appl_method_cd',
                        '.input_01 > tr:nth-child(7) > td > a > *.icon_img::attr(alt), .input_01 > tbody > tr:nth-child(7) > td > a > .icon_img::attr(alt)',
                        []),
                    Field(
                        'link_url',
                        #'.input_01 > tr:nth-child(7) > td > a::attr(onclick), .input_01 > tbody > tr:nth-child(7) > td > a::attr(onclick)',
                        '.input_01 > tr:nth-child(7) > td > a, .input_01 > tbody > tr:nth-child(7) > td > a',
                        #'.input_01 > tr:nth-child(7) > td > a::attr(href), .input_01 > tbody > tr:nth-child(7) > td > a::attr(href)',
                        []),
                    Field(
                        'job_ability_course',
                        '.input_01 > tr:nth-child(8) > td:nth-child(2) *::text, .input_01 > tbody > tr:nth-child(8) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'cb_eval_accept',
                        '.input_01 > tr:nth-child(8) > td:nth-child(4) *::text, .input_01 > tbody > tr:nth-child(8) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'all_eval_accept',
                        '.input_01 > tr:nth-child(9) > td:nth-child(2) *::text, .input_01 > tbody > tr:nth-child(9) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'lang_cd',
                        '.input_01 > tr:nth-child(9) > td:nth-child(4) *::text, .input_01 > tbody > tr:nth-child(9) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'vsl_handicap_supp',
                        '.input_01 > tr:nth-child(10) > td:nth-child(2) *::text, .input_01 > tbody > tr:nth-child(10) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'hrg_handicap_supp',
                        '.input_01 > tr:nth-child(10) > td:nth-child(4) *::text, .input_01 > tbody > tr:nth-child(10) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'course_desc',
                        '.input_01 > tr:nth-child(11) > td *::text, .input_01 > tbody > tr:nth-child(11) > td *::text',
                        [])])]]

    def parse_item(self, response, *args, **kw):

        #print('===>')
        #print(args)
        #print(kw)
        #print('===>')
        links = response.xpath("//a/@onclick[contains(.,'selectRow')]")
        locations = response.xpath("//div[contains(@class, 'lectureCont')]/ul/li[1]/dl/dd/text()")
        for link, location in zip(links, locations):
            #num = link.re("'(.*)'")
            num = link.re("\((.+?)\)")
            url = 'https://www.e-room.or.kr/gw/portal/org_lecture_info?mode=read&leccode='+num[0]+'&page_no=1&selectRegion=&gubun=&studyKind=&searchKeyWord=&searchFromDate=&searchEndDate='
            #print(num, location.get())
            yield Request(url, self.parse_item, cb_kwargs={'location': location.get()})
            #print(link.data)
        #for location in locations:
            #print(location.get())
        links = response.xpath("//script")
        for link in links:
            #page = link.re("pagingFunc\((.+?)\)")
            #page = link.re(".*")
            page = link.re("generatePaging\('(.+?)', '(.+?)', '(.+?)'\)")
            if len(page) == 3:
                print(page)
                #print(page[1])
                #n = int(page[1])
                #print(n)
                for i in range(1, int(page[1])+1):
                #for i in range(1, 2):
                    url = 'https://www.e-room.or.kr/gw/portal/org_lecture_info?mode=list&leccode=&page_no=' \
                        +str(i) \
                        +'&selectRegion=&gubun=&studyKind=&searchKeyWord=&searchFromDate=&searchEndDate='
                    #print(url)
                    yield Request(url, self.parse_item)

        for sample in self.items:
            items = []
            itemUrl = response.url
            if itemUrl.find("mode=read") > 0:  # 상세URL만 읽음
                try:
                    for definition in sample:
                        items.extend(
                            [i for i in self.load_item(definition, response)]
                        )
                except RequiredFieldMissing as exc:
                    self.logger.warning(str(exc))
                if items:
                    for item in items:
                        if 'location' in kw.keys():
                            item['sigungu_cd'] = kw['location']
                        if 'link_url' in item.keys():
                            for link_url in item['link_url']:
                                online = Selector(text=link_url).xpath('//a/@href').get()
                                offline = Selector(text=link_url).xpath('//a/@onclick').get()
                                if online is not None and online != 'http://':
                                    item['link_url'] = online
                                    break
                                elif offline is not None:
                                    inst_ids = re.search(r'visitOrgFunc\((.*)\)', offline)
                                    if inst_ids is not None:
                                        item['link_url'] = 'https://www.e-room.or.kr/gw/portal/org_info?mode=read&orgcode='+inst_ids.group(1)
                            if type(item['link_url']) is list:
                                item['link_url'] = itemUrl
                            #print(f"link_url = {item['link_url']}")
                        # item['url'] = response.url
                        leccodeidx = re.search(r"leccode=([^&]*)", itemUrl)
                        item['url'] = itemUrl  # URL
                        item['inst_id'] = None  # 기관ID
                        item['course_id'] = leccodeidx.group(1)  # 강좌ID
                        item['course_id_org'] = leccodeidx.group(1)

                        #유효성 check
                        if 'course_nm' not in item.keys() and  'org' not in item.keys():
                            self.logger.warning('Gangwon Course validation check failed. skipping...')
                            continue

                        course_period = re.match('(\d{4}-\d{2}-\d{2})~(\d{4}-\d{2}-\d{2})', re.sub('[ ]', '', item['course_period']))   # 강좌기간
                        register_period = re.match('(\d{4}-\d{2}-\d{2})~(\d{4}-\d{2}-\d{2})',re.sub('[ ]', '', item['register_period']))  # 접수기간

                        if course_period != None:   # 강좌시작일, 강좌종료일
                            item['course_start_dt'] = course_period.group(1)
                            item['course_end_dt'] = course_period.group(2)
                        if register_period != None: # 접수시작일, 접수종료일
                            item['receive_start_dt'] = register_period.group(1)
                            item['receive_end_dt'] = register_period.group(2)
                        if item['job_ability_course'] == '훈련기간': # 직업능력강좌여부
                            item['job_ability_course_yn'] = 'Y'
                        else:
                            item['job_ability_course_yn'] = 'N'
                        if item['cb_eval_accept'] == '인정기관': # 학점은행제평가인정여부
                            item['cb_eval_accept_yn'] = 'Y'
                        else:
                            item['cb_eval_accept_yn'] = 'N'
                        if item['all_eval_accept'] == '인정기관':  # 평생학습계좌제평가인정여부
                            item['all_eval_accept_yn'] = 'Y'
                        else:
                            item['all_eval_accept_yn'] = 'N'
                        if item['vsl_handicap_supp'] == '지원':   # 시각장애지원여부
                            item['vsl_handicap_supp_yn'] = 'Y'
                        else:
                            item['vsl_handicap_supp_yn'] = 'N'
                        if item['hrg_handicap_supp'] == '지원':   # 청각장애지원여부
                            item['hrg_handicap_supp_yn'] = 'Y'
                        else:
                            item['hrg_handicap_supp_yn'] = 'N'

                        # 초기값edu_target_cd
                        keyarray = ['teacher_pernm', 'enroll_amt', 'edu_method_cd', 'edu_cycle_content'
                                    , 'edu_location_desc', 'inquiry_tel_no', 'edu_quota_cnt', 'edu_quota_cnt'
                                    , 'lang_cd', 'edu_target_cd', 'course_desc', 'link_url', 'enroll_appl_method_cd']
                        '''
                        if 'link_url' in item.keys() and type(item['link_url']) is list:
                            item['link_url'] = item['link_url'][0]
                            inst_ids = re.search(r'visitOrgFunc\((.*)\)', item['link_url'])
                            if inst_ids is not None:
                                item['link_url'] = 'https://www.e-room.or.kr/gw/portal/org_info?mode=read&orgcode='+inst_ids.group(1)
                        '''
                        for keyitem in keyarray:
                            try:
                                item[keyitem] = item[keyitem].strip()
                                if keyitem == 'lang_cd':
                                    item[keyitem] = item[keyitem].lower()
                                if keyitem == 'enroll_appl_method_cd':
                                    item['enroll_appl_method_cd'] = re.sub('.gif', '', re.sub(r'\S*_', '', item['enroll_appl_method_cd']))
                            except KeyError:
                                if keyitem == 'edu_location_desc':
                                    item[keyitem] = ''
                                else:
                                    item[keyitem] = None

                        dt = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))
                        item['date'] = "%s:%.3f%s" % (
                            dt.strftime('%Y-%m-%dT%H:%M'),
                            float("%.3f" % (dt.second + dt.microsecond / 1e6)),
                            dt.strftime('%z')
                        )
                        yield item
                    break
