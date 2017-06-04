import re

import requests
from bs4 import BeautifulSoup


class Episode:
    """
    Episode에 대한 정보를 가지고 있는다.
    """

    def __init__(self, episode_num, episode_thumbnail, episode_title, episode_rating, episode_date):
        self._episode_number = episode_num
        self._episode_thumnail_url = episode_thumbnail
        self._episode_title = episode_title
        self._episode_rating = episode_rating
        self._episode_date = episode_date
        self._episode_images = []

    @property
    def episode_number(self):
        return self._episode_number

    @property
    def episode_thumbnail_url(self):
        return self._episode_thumnail_url

    @property
    def episode_title(self):
        return self._episode_title

    @property
    def episode_rating(self):
        return self._episode_rating

    @property
    def episode_date(self):
        return self._episode_date

    @property
    def episode_images(self):
        return self._episode_images


class NaverWebToonCrawler:
    def __init__(self, webtoonID=654774):
        self.list_url = "http://comic.naver.com/webtoon/list.nhn?" \
                        "titleId={webtoon_Id}&" \
                        "page={page}"
        self.detail_list_url = "http://comic.naver.com/webtoon/detail.nhn" \
                               "?titleId={webtoonID}" \
                               "&no={episode_num}"
        self.webtoon_id = webtoonID
        self.page = 1
        response = requests.get(
            self.list_url.format(
                webtoon_Id=self.webtoon_id, page=1)
        )
        dom = BeautifulSoup(response.text, "lxml")
        pattern = re.compile(r"no=(\d*)")
        temp = NaverWebtoon(self.webtoon_id)
        self.name_dict = {
            self.webtoon_id: temp.title
        }

        self.webtoon_list = {
            self.name_dict[self.webtoon_id]: temp
        }  # ex) 소녀의 세계, 유미의 세포들
        self.episode_end_number = \
            int(pattern.findall(dom.select_one("table") \
                                .select("tr", )[1] \
                                .select_one("a").attrs.get("href")
                                )[0]
                )

    def get_episode_end_number(self):
        response = requests.get(self.list_url.format(self.webtoon_id, 1))
        dom = BeautifulSoup(response.text, "lxml")
        pattern = re.compile(r"no=(\d*)")
        self.episode_end_number = \
            int(pattern.findall(dom.select_one("table") \
                                .find_all("tr", recursive=False)[0] \
                                .select_one("a").attrs.get("href")
                                )[0]
                )

    def crawling_page(self, page_num=1):
        """
        webtoon의 한 페이지를 크롤링한다.
        :param page_num: crawling 할 페이지 
        :return: 
        """
        response = requests.get(
            self.list_url.format(
                webtoon_Id=self.webtoon_id, page=page_num)
        )
        dom = BeautifulSoup(response.text, "lxml")
        temp_dict = {}
        if self.episode_end_number > 0 and 0 < page_num < self.episode_end_number:
            toons = dom.select_one("table").select("tr")
            pattern = re.compile(r"no=(\d*)")
            for toon in toons[:0:-1]:  # td단위
                temp = toon.select("td")
                number = int(
                    pattern.findall(
                        temp[0].select_one("a").attrs.get("href")
                    )[0]
                )
                thumb_url = temp[0].select_one("img").attrs.get("src")
                title = temp[1].text.strip()
                rating = float(temp[2].select_one("strong").text)
                date = temp[3].text
                e = Episode(number, thumb_url, title, rating, date)
                temp_dict.update({e.episode_number: e})
            self.webtoon_list[self.name_dict[self.webtoon_id]].add_episode(temp_dict)

    def crawling_all_pages(self):
        for n in range(self.episode_end_number, 0, -1):
            self.crawling_page(n)

    def crawling_episode(self, episode_num):
        response = requests.get(
            self.detail_list_url.format(
                webtoonID=self.webtoon_id, episode_num=episode_num)
        )
        dom = BeautifulSoup(response.text, "lxml")
        img_list = dom.select_one("div.wt_viewer").select("img")
        temp_list = []
        for img in img_list:
            temp_list.append(img.attrs.get("src"))
        self.webtoon_list[self.name_dict[self.webtoon_id]] \
            .episodes[episode_num].episode_images.extend(temp_list)
        print(self.webtoon_list[self.name_dict[self.webtoon_id]] \
              .episodes[episode_num].episode_images)

    def print_webtoon(self, webtoon_id=654774):
        self.webtoon_list[self.name_dict[webtoon_id]].print_episodes()


class NaverWebtoon:
    """
    NaverWebtoon 작품 1개를 의미하는 class
    1. 작품명 
    2. 작가명
    3. 썸네일 
    4. 설명
    """

    def __init__(self, webtoon_id):
        self.webtoon_url = "http://comic.naver.com/webtoon/list.nhn?" \
                           "titleId={webtoon_Id}&" \
                           "page=1"
        self.webtoon_id = webtoon_id
        response = requests.get(
            self.webtoon_url.format(
                webtoon_Id=self.webtoon_id)
        )
        dom = BeautifulSoup(response.text, "lxml")
        title_thumbnail = dom.select_one("div.thumb").select_one("img")
        writer_explain = dom.select_one("div.detail")

        self.title = title_thumbnail.attrs.get("title")
        self.writer = writer_explain.select_one("span.wrt_nm").text.strip()
        self.thumbnail_url = title_thumbnail.attrs.get("src")
        self.explain = writer_explain.select_one("p").text
        self.episodes = {}

    def __get_init_info(self):
        response = requests.get(self.webtoon_url.format(self.webtoon_id))
        dom = BeautifulSoup(response.text, "lxml")
        title_thumbnail = dom.select_one("div.thumb").select_one("img")
        writer_explain = dom.select_one("div.detail")

        self.title = title_thumbnail.attrs.get("title")
        self.thumbnail_url = title_thumbnail.attrs.get("src")
        self.writer = writer_explain.select_one("span.wrt_nm").text.strip()
        self.explain = writer_explain.select_one("p").text

    def add_episode(self, Episodes):
        try:
            self.episodes.update(Episodes)
        except Exception as ex:
            print(ex)

    def print_episodes(self):
        for e, n in self.episodes.items():
            print(e, " ", n.episode_thumbnail_url)
        print("end")


crawl = NaverWebToonCrawler(webtoonID=654774)
crawl.crawling_all_pages()
crawl.print_webtoon()
crawl.crawling_episode(102)
