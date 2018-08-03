# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import ItjuziItem


class ItjuziSpider(scrapy.Spider):
    name = "itjuzi"
    allowed_domains = ["itjuzi.com"]
    base_url = 'https://www.itjuzi.com/company/'
    start_urls = [base_url + str(page) for page in range(1, 11)]
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.itjuzi.com",
        "If-Modified-Since": "Wed, 25 Jul 2018 07:58:00 GMT",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    }
    cookies = {
        "gr_user_id": "4c65a320-54b4-4724-afc5-f5de000c5c9c",
        "acw_tc": "AQAAAD7pv0E9CwIARkDttwEIzNdy+XKF",
        "session": "b05b6a22fb39b2e17d8630595c016b0cf9337e6f",
        "Hm_lvt_1c587ad486cdb6b962e94fc2002edf89": "1531552536,1532501975",
        "MEIQIA_VISIT_ID": "17rjBuxsPpuYzgg1jODPbGZDf7P",
        "MEIQIA_EXTRA_TRACK_ID": "17rjBzYTPqDziVWRx0G9pI6tkyA",
        "identity": "15768856976%40test.com",
        "unique_token": "602418",
        "remember_code": "wC5yPAKJBU",
        "Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89": "1532505480",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse)

    def parse(self, response):
        if response.status == 200:
            item = ItjuziItem()
            soup = BeautifulSoup(response.body, "lxml")

            part1 = soup.find(class_="picinfo")
            item["company_name"] = part1.find(class_="seo-important-title").get("data-name")
            item["company_slogan"] = part1.find(class_="seo-slogan").string
            item["company_info"] = part1.find(class_="scope c-gray-aset").string
            item["main_page"] = part1.find(class_="link-line").find(target="_blank").get("href")

            item["company_intro"] = \
            soup.find(class_="block-inc-info on-edit-hide").find(class_="block").find_all("div")[-1].get_text().strip()

            part2 = soup.find("tbody").find_all("tr")
            if part2:
                financing_set = []
                for ele in part2:
                    info = {}
                    td_list = ele.find_all("td")
                    if len(td_list) < 4:
                        break
                    info["financing_time"] = td_list[0].get_text().strip()
                    info["financing_level"] = td_list[1].get_text().strip()
                    info["financing_amount"] = td_list[2].get_text().strip()
                    info["financing_company"] = td_list[3].get_text().strip()
                    financing_set.append(info)
                item["financing_list"] = financing_set

            part3 = soup.find_all(class_="list-round-v2")[1].tbody.find_all("tr") if len(
                soup.find_all(class_="list-round-v2")) > 1 else []
            if part3:
                ext_financing_set = []
                for ele in part3:
                    info = {}
                    td_list = ele.find_all("td")
                    if len(td_list) != 4:
                        break
                    info["ext_financing_company"] = td_list[0].get_text().strip()
                    info["ext_financing_level"] = td_list[1].get_text().strip() if td_list else ""
                    info["ext_financing_amount"] = td_list[2].get_text().strip()
                    info["ext_financing_time"] = td_list[3].get_text().strip()
                    ext_financing_set.append(info)
                item["ext_financing_set"] = ext_financing_set

            part4 = soup.find(class_="product-list")
            if part4:
                li_list = part4.find_all("li")

                info_list = []
                for li in li_list:
                    info = {}
                    info['product_name'] = li.find(class_='product-name').get_text().strip()
                    info['product_info'] = li.find(class_='product-des').get_text().strip()
                    info_list.append(info)

                item['product'] = info_list
            item["company_url"] = response.url
            yield item
