from __future__ import absolute_import

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity
from scrapy.spiders import Rule

from ..utils.spiders import BasePortiaSpider
from ..utils.starturls import FeedGenerator, FragmentGenerator
from ..utils.processors import Item, Field, Text, Number, Price, Date, Url, Image, Regex
from ..items import PortiaItem, InstItemItem

import pytz, datetime, re
import hashlib

class GileOrKr(BasePortiaSpider):
    name = "www.gile.or.kr.inst"
    allowed_domains = ['www.gile.or.kr']
    start_urls = [
        #'http://www.gile.or.kr/web/organ/view.do?mId=71&page=1&organIdx=748500001']
        'http://www.gile.or.kr/web/organ/list.do?mId=71&page=1']
    rules = [
        Rule(
            LinkExtractor(
                allow=('www.gile.or.kr\\/web\\/organ\\/list.do\\?mId=71&page=\d'),
                #allow=('www.gile.or.kr\\/web\\/organ\\/list.do\\?mId=71&page=1$'),
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
                '#cms_organ_article',
                [
                    Field(
                        'inst_nm',
                        'h2.title *::text',
                        []),
                    Field(
                        'inst_ceo_pernm',
                        'div:nth-child(3) > .viewTypeA > tr:nth-child(1) > td:nth-child(2) *::text, div:nth-child(3) > .viewTypeA > tbody > tr:nth-child(1) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'inst_set_up_main_agent',
                        'div:nth-child(3) > .viewTypeA > tr:nth-child(1) > td:nth-child(4) *::text, div:nth-child(3) > .viewTypeA > tbody > tr:nth-child(1) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'establishment_dt',
                        'div:nth-child(3) > .viewTypeA > tr:nth-child(2) > td:nth-child(2) *::text, div:nth-child(3) > .viewTypeA > tbody > tr:nth-child(2) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'inst_operation_status_cd',
                        'div:nth-child(3) > .viewTypeA > tr:nth-child(2) > td:nth-child(4) *::text, div:nth-child(3) > .viewTypeA > tbody > tr:nth-child(2) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'tel_no',
                        'div:nth-child(3) > .viewTypeA > tr:nth-child(3) > td:nth-child(2) *::text, div:nth-child(3) > .viewTypeA > tbody > tr:nth-child(3) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'fax_no',
                        'div:nth-child(3) > .viewTypeA > tr:nth-child(3) > td:nth-child(4) *::text, div:nth-child(3) > .viewTypeA > tbody > tr:nth-child(3) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'manager_pernm',
                        'div:nth-child(3) > .viewTypeA > tr:nth-child(4) > td:nth-child(2) *::text, div:nth-child(3) > .viewTypeA > tbody > tr:nth-child(4) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'homepage_url',
                        'div:nth-child(3) > .viewTypeA > tr:nth-child(4) > td:nth-child(4) *::text, div:nth-child(3) > .viewTypeA > tbody > tr:nth-child(4) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'email',
                        'div:nth-child(3) > .viewTypeA > tr:nth-child(5) > td:nth-child(2) *::text, div:nth-child(3) > .viewTypeA > tbody > tr:nth-child(5) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'inst_operation_form',
                        'div:nth-child(3) > .viewTypeA > tr:nth-child(5) > td:nth-child(4) *::text, div:nth-child(3) > .viewTypeA > tbody > tr:nth-child(5) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'address',
                        'div:nth-child(3) > .viewTypeA > tr:nth-child(6) > td *::text, div:nth-child(3) > .viewTypeA > tbody > tr:nth-child(6) > td *::text',
                        []),
                    Field(
                        'inst_desc',
                        'div:nth-child(3) > .viewTypeA > tr:nth-child(7) > td *::text, div:nth-child(3) > .viewTypeA > tbody > tr:nth-child(7) > td *::text',
                        [])])]]


    def parse_item(self, response):

        links = response.xpath("//td[@class='subject mapInfo']/a/@href")

        for link in links:
            href = link.extract()

            url = "http://www.gile.or.kr/web/organ/" + href
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
                        organidx = re.search(r"organIdx=([^&]*)", itemUrl)

                        organId = organidx.group(1)
                        hash = hashlib.sha1(f'{organId}'.encode('UTF-8')).hexdigest()
                        item['inst_id'] = hash[:14] # 기관ID(hash)
                        item['inst_id_org'] = organId  # 기관ID(원형)
                        item['url'] = itemUrl  # URL

                        #유효성 check
                        if 'inst_nm' not in item.keys() :
                            self.logger.warning('Gyeongbuk Inst validation check failed. skipping...')
                            continue

                        address = re.search(r"\((.*?)\)(.*)", re.sub(r"[\xa0]", " ", item['address']))     # 주소

                        if address == None:
                            item['zipcode'] = None
                            item['addr1'] = item['address'].strip()
                        else:
                            item['zipcode'] = address.group(1)
                            item['addr1'] = address.group(2).strip()

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
                            if item['inst_operation_form'] == '직영':
                                item['inst_operation_form_cd'] = '01'
                            elif item['inst_operation_form'] == '위탁':
                                item['inst_operation_form_cd'] = '02'
                            elif item['inst_operation_form'] == '병행':
                                item['inst_operation_form_cd'] = '03'
                            elif item['inst_operation_form'].strip() == '':
                                item['inst_operation_form_cd'] = None
                            else:   # 그 외
                                item['inst_operation_form_cd'] = '04'
                        except KeyError:
                            item['inst_operation_form_cd'] = None

                        try:    # 설립일
                            if item['establishment_dt'].strip() == '':
                                item['establishment_dt'] = None
                        except KeyError:
                            item['establishment_dt'] = None

                        # 초기값
                        keyarray = ['inst_ceo_pernm', 'manager_pernm', 'tel_no', 'fax_no', 'email', 'homepage_url']

                        for keyitem in keyarray:
                            try:
                                item[keyitem] = item[keyitem].strip()
                            except KeyError:
                                item[keyitem] = None

                        dt = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))
                        item['date'] = "%s:%.3f%s" % (
                            dt.strftime('%Y-%m-%dT%H:%M'),
                            float("%.3f" % (dt.second + dt.microsecond / 1e6)),
                            dt.strftime('%z')
                        )
                        yield item
                    break