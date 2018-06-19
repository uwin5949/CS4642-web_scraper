import scrapy


class DataSpider(scrapy.Spider):
    name = "house"
    start_urls = [
        'http://www.hitad.lk/EN/property?page=0',
    ]

    def parse(self, response):
        for item in response.css('ul.cat-ads'):
            location =item.css('div.item-facets2::text').extract_first()
            if(location !=None):
                location = location.lstrip().rstrip()
            else:
                location = "None"

            dataList = item.css('div.item-facets::text').extract()


            if(len(dataList)>=4):
                propertyType = dataList[3]
            else:
                propertyType = "None"
            if(len(dataList)>=3):
                subCategory = dataList[2]
            else:
                subCategory = "None"
            yield {
                'title': item.css('h4.fw_b::text').extract_first().lstrip().rstrip(),
                'price': item.css('span.list-price-value::text').extract_first(),
                'type': dataList[0],
                'category': dataList[1],
                'subCategory': subCategory,
                'propertyType': propertyType,
                'location': location,
            }

        next_page = response.css('div.af_nextback a::attr(href)').extract()[-2]
        print("=================================")
        print(next_page)
        print("=================================")
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)