# -*- coding: utf-8 -*-
import datetime
import hashlib
import logging
import time
from logging import handlers

import pandas as pd
from bs4 import BeautifulSoup
from db.alchemy import alchemy
from selenium import helper


# log setting
carLogFormatter = logging.Formatter("%(asctime)s,%(message)s")

carLogHandler = handlers.TimedRotatingFileHandler(
    filename="log/scrap.log",
    when="midnight",
    interval=1,
    encoding="utf-8",
)
carLogHandler.setFormatter(carLogFormatter)
carLogHandler.suffix = "%Y%m%d"

scarp_logger = logging.getLogger()
scarp_logger.setLevel(logging.INFO)
scarp_logger.addHandler(carLogHandler)


# content processing
def content_replacing(text):
    result = str(text).replace("ⓒPixabay", "").replace("\n\n", "\n").replace("\n", "")

    return result


# date processing
def date_str_to_date(str_date):
    if str_date == "" or str_date == " " or str_date is None:
        str_date = str(datetime.datetime.now())
        str_date = str_date[:19]
        str_date = datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")

    elif str_date.endswith("일전"):
        datenum = str_date.replace("일전", "").replace(" ", "")
        str_date = str(datetime.datetime.now() - datetime.timedelta(days=int(datenum)))
        str_date = str(str_date[:11]) + "00:00:00"

    elif str_date.endswith("시간전"):
        datenum = str_date.replace("시간전", "").replace(" ", "")
        str_date = str(datetime.datetime.now() - datetime.timedelta(hours=int(datenum)))
        str_date = str(str_date[:19])

    elif str_date.endswith("분전"):
        datenum = str_date.replace("분전", "").replace(" ", "")
        str_date = str(datetime.datetime.now() - datetime.timedelta(minutes=int(datenum)))
        str_date = str(str_date[:19])

    else:
        if str_date.startswith("기사입력"):
            str_date = str_date.replace("기사입력 ", "")
        str_date = str_date.replace("오전", "AM").replace("오후", "PM").replace("오 전", "AM").replace("오 후", "PM")
        str_date = datetime.datetime.strptime(str_date, "%Y.%m.%d. %p %I:%M").strftime("%Y-%m-%d %H:%M:%S")

    return str(str_date)


# naver crawling
def naver_crawling():
    # category_dict
    category_dict = {
        "200100": "100",
        "200101": "101",
        "200102": "102",
        "200103": "103",
        "200105": "105",
        "200106": "106",
        "200107": "107",
    }
    time.sleep(3)
    naver_helper.driver.implicitly_wait(10)

    loop = True
    while loop:
        try:
            for key in category_dict:
                list_con = []
                logging.info(str(key) + " naver start")
                category_url = (
                    "https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1="
                    + str(category_dict[key])
                    + "&listType=summary"
                )
                naver_helper.go_to(category_url)

                # beautifulsoup 사용
                soup = BeautifulSoup(naver_helper.driver.page_source, "html.parser")
                news_url = list(
                    dict.fromkeys(
                        [url["href"] for url in soup.find_all("a", attrs={"class": "nclicks(fls.list)"})]
                    )
                )

                for url in news_url:
                    naver_helper.go_to(url)

                    if key == "200106":
                        title = naver_helper.get_text_by_xpath("/html/body/div/div[3]/div[1]/div/h2")

                        body = naver_helper.get_text_by_xpath("/html/body/div/div[3]/div[1]/div/div[4]/div")
                        body = content_replacing(body)

                        # create_date
                        dummyDate = naver_helper.get_text_by_xpath(
                            "/html/body/div/div[3]/div[1]/div/div[2]/span/em"
                        )
                        createDate = date_str_to_date(dummyDate)

                        # image_url
                        image_url = naver_helper.get_attribute_by_xpath(
                            "/html/body/div/div[3]/div[1]/div/div[4]/div/span[1]/span/img",
                            "src",
                        )
                        if not image_url:
                            image_url = naver_helper.get_attribute_by_xpath(
                                "/html/body/div/div[3]/div[1]/div/div[4]/div/span/span/img",
                                "src",
                            )
                        else:
                            image_url = image_url

                        if not image_url:
                            image_url = "no image"

                        # urlmd5
                        urlmd5 = hashlib.md5(url.encode("utf-8")).hexdigest()

                        # media
                        media = naver_helper.get_attribute_by_xpath(
                            "/html/body/div/div[3]/div[1]/div/div[1]/a/img",
                            "alt",
                        )

                    elif key == "200107":
                        title = naver_helper.get_text_by_xpath(
                            "/html/body/div[2]/div[1]/div/div/div[1]/div/div[1]/h4"
                        )
                        if not title:
                            title = naver_helper.get_text_by_xpath(
                                "/html/body/div[2]/div[2]/div/div/div[1]/div/div[1]/h4"
                            )

                        body = naver_helper.get_text_by_xpath(
                            "/html/body/div[2]/div[1]/div/div/div[1]/div/div[3]"
                        )
                        if not body:
                            body = naver_helper.get_text_by_xpath(
                                "/html/body/div[2]/div[2]/div/div/div[1]/div/div[3]"
                            )
                        body = content_replacing(body)

                        # create_date
                        dummyDate = naver_helper.get_text_by_xpath(
                            "/html/body/div[2]/div[2]/div/div/div[1]/div/div[1]/div/span[1]"
                        )
                        createDate = date_str_to_date(dummyDate)

                        # image_url
                        image_url = naver_helper.get_attribute_by_xpath(
                            "/html/body/div[2]/div[2]/div/div/div[1]/div/div[3]/span/img",
                            "src",
                        )
                        if not image_url:
                            image_url = naver_helper.get_attribute_by_xpath(
                                "/html/body/div[2]/div[1]/div/div/div[1]/div/div[3]/span/img",
                                "src",
                            )
                        else:
                            image_url = image_url

                        if not image_url:
                            image_url = "no image"

                        # urlmd5
                        urlmd5 = hashlib.md5(url.encode("utf-8")).hexdigest()

                        # media
                        media = naver_helper.get_attribute_by_xpath(
                            "/html/body/div[2]/div[2]/div/div/div[1]/div/div[1]/span/a/img",
                            "alt",
                        )

                    else:
                        title = naver_helper.get_text_by_xpath(
                            "/html/body/div[2]/table/tbody/tr/td[1]/div/div[1]/div[3]/h3"
                        )

                        body = naver_helper.get_text_by_xpath(
                            "/html/body/div[2]/table/tbody/tr/td[1]/div/div[2]/div[1]"
                        )
                        body = content_replacing(body)

                        # create_date
                        dummyDate = naver_helper.get_text_by_xpath(
                            "/html/body/div[2]/table/tbody/tr/td[1]/div/div[1]/div[3]/div/span[2]"
                        )
                        createDate = date_str_to_date(dummyDate)

                        # image_url
                        image_url = naver_helper.get_attribute_by_xpath(
                            "/html/body/div[2]/table/tbody/tr/td[1]/div/div[2]/div[1]/span[1]/img",
                            "src",
                        )
                        if not image_url:
                            image_url = naver_helper.get_attribute_by_xpath(
                                "/html/body/div[2]/table/tbody/tr/td[1]/div/div[2]/div[1]/span[2]/img",
                                "src",
                            )
                        else:
                            image_url = image_url

                        if not image_url:
                            image_url = "no image"

                        media = naver_helper.get_attribute_by_xpath(
                            "/html/body/div[2]/table/tbody/tr/td[1]/div/div[1]/div[1]/a/img",
                            "alt",
                        )

                        # urlmd5
                        urlmd5 = hashlib.md5(url.encode("utf-8")).hexdigest()

                    list_con.append(
                        {
                            "url": url,
                            "title": title,
                            "content": body,
                            "create_date": createDate,
                            "kind": key,
                            "url_md5": urlmd5,
                            "image_url": image_url,
                            "portal": "naver",
                            "media": media,
                        }
                    )
                    naver_helper.back()
                logging.info(str(key) + " naver end")
                totalSql = pd.DataFrame(
                    list_con,
                )
                totalSql.drop_duplicates()
                list_con.clear()

                # dataframe to_sql database insert
                alchemy.DataSource("mysql", "news_scraper").df_to_sql(totalSql, "naver_news")
                del totalSql

        except Exception as e:
            logging.info(e)
            naver_helper.driver.close()
            naver_helper.driver.quit()

            loop = False


if __name__ == "__main__":
    with helper.Helper(
        "https://news.naver.com/main/list.naver?mode=LSD&mid=sec&listType=paper",
        timeout=1,
    ) as naver_helper:
        # naver crawling
        totalSql = naver_crawling()
