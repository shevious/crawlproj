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
import logging

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
                #allow=('www\\.uill\\.or\\.kr\\/UR\\/info\\/lecture\\/list\\.do\\?rbsIdx=34&page=\d'),
                #allow=('www\\.uill\\.or\\.kr\\/UR\\/info\\/lecture\\/view.do\\?rbsIdx=34\\&page=1\\&organIdx=3175\\&idx=EX18651'),
                # page1 만 하기 위함
                allow=('www\\.uill\\.or\\.kr\\/UR\\/info\\/lecture\\/list\\.do\\?rbsIdx=34&page=1$'),
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
                        'title',
                        'h2 *::text',
                        []),
                    Field(
                        'lecturer',
                        '.cle > table > tr:nth-child(5) > td:nth-child(2) *::text, .cle > table > tbody > tr:nth-child(3) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'period',
                        '.cle > table > tr:nth-child(4) > td:nth-child(2) *::text, .cle > table > tbody > tr:nth-child(2) > td:nth-child(2) *::text',
                        []),
                    Field(
                        'org',
                        '.cle > table > tr:nth-child(3) > td *::text, .cle > table > tbody > tr:nth-child(1) > td *::text',
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
            #print('#### yield')
            #print(url)
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
                    #print(f'print parse_item in pipeline: title={item["title"]}')
                    #logging.info(f'####info parse_item in pipeline: title={item["title"]}')
                    #logging.debug(f'####debug parse_item in pipeline: title={item["title"]}')
                    yield item
                break

