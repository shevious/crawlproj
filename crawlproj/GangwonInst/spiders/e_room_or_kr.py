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
from ..items import PortiaItem, InstItem

import pytz, datetime, re

class ERoomOrKr(BasePortiaSpider):
    name = "www.e-room.or.kr.inst"
    allowed_domains = ['www.e-room.or.kr']
    start_urls = [
        'https://www.e-room.or.kr/gw/portal/org_info?mode=list&orgcode=&page_no=1&selectRegion=&keyword=']
    rules = [
        Rule(
            LinkExtractor(
                allow=('www.e-room.or.kr\\/gw\\/portal\\/org_info\\?'),
                deny=()
            ),
            callback='parse_item',
            follow=True
        )
    ]
    items = [
        [
            Item(
                InstItem,
                None,
                '.type01',
                [
                    Field(
                        'inst_nm',
                        'tr:nth-child(1) > td:nth-child(2) *::text, tbody > tr:nth-child(1) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'inst_ceo_pernm',
                        'tr:nth-child(1) > td:nth-child(4) *::text, tbody > tr:nth-child(1) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'tel_no',
                        'tr:nth-child(2) > td:nth-child(2) *::text, tbody > tr:nth-child(2) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'fax_no',
                        'tr:nth-child(2) > td:nth-child(4) *::text, tbody > tr:nth-child(2) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'manager_pernm',
                        'tr:nth-child(3) > td:nth-child(2) *::text, tbody > tr:nth-child(3) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'homepage_url',
                        'tr:nth-child(3) > td:nth-child(4) *::text, tbody > tr:nth-child(3) > td:nth-child(4) *::text',
                        []),
                    Field(
                        'addr1',
                        'tr:nth-child(4) > .textL *::text, tbody > tr:nth-child(4) > .textL *::text',
                        []),
                    Field(
                        'inst_desc',
                        'tr:nth-child(7) > .textL *::text, tbody > tr:nth-child(7) > .textL *::text',
                        [])])]]

    def parse_item(self, response):
        links = response.xpath("//a/@onclick[contains(.,'selectRow')]")
        for link in links:
            num = link.re("\((.+?)\)")
            url = 'https://www.e-room.or.kr/gw/portal/org_info?mode=read&orgcode='+num[0]+'&page_no=1&selectRegion=&keyword='
            yield Request(url, self.parse_item)

        links = response.xpath("//script")
        for link in links:
            #page = link.re(".*")
            page = link.re("generatePaging\('(.+?)', '(.+?)', '(.+?)'\)")
            if len(page) == 3:
                #print(page[1])
                for i in range(1, int(page[1]) +1):
                    url = 'https://www.e-room.or.kr/gw/portal/org_info?mode=list&orgcode=&page_no=' \
                        +str(i) \
                        +'&selectRegion=&keyword='
                    yield Request(url, self.parse_item)

        for sample in self.items:
            items = []

            base_url = get_base_url(response)
            if base_url.find("mode=read") > 0:

                try:
                    for definition in sample:
                        items.extend(
                            [i for i in self.load_item(definition, response)]
                        )
                except RequiredFieldMissing as exc:
                    self.logger.warning(str(exc))
                if items:
                    for item in items:
                        itemUrl = response.url
                        orgidx = re.search(r"orgcode=([^&]*)", itemUrl)
                        item['url'] = itemUrl  # URL
                        item['inst_id'] = orgidx.group(1)  # 기관ID

                        # 초기값
                        keyarray = ['inst_ceo_pernm', 'manager_pernm', 'tel_no', 'fax_no', 'email', 'homepage_url',
                                    'establishment_dt', 'inst_set_up_main_agent_cd', 'inst_operation_form_cd',
                                    'inst_operation_status_cd', 'zipcode', 'inst_desc']
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
