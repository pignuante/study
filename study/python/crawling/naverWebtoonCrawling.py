import re
import requests
from bs4 import BeautifulSoup


class NaverWebtoonCrawler:
    def __init__(self, webtoonID=654774, page=1):
        self.base_url = "http://comic.naver.com/webtoon/list.nhn"
        self.base_detail_url = "http://comic.naver.com/webtoon/detail.nhn"
        self.webtoonID = webtoonID
        self.page = page
        self.episodes = []
        self.episode_num = 0
        self.__params = {
                'titleId': self.webtoonID,
                'page': self.page,
                }  # 기본 시작은 1
        self.response = requests.get(self.base_url, self.__params)

    def print_episodes(self):
        for e in self.episodes:
            print(e.title)

    def thumnail(self, text):
        """
        text로 받은 주소를 기반, episode의 thumnail의 이미지를 리턴한다.
        :param text: table>tbody>tr의 정보가 온다.(str) 
        :return: tr>td>img의 herf주소를 리턴. 없을 시 None을 리턴
        """
        return text.select_one("a").attrs.get("href")

    def title(self, text):
        """
        text로 받은 주소를 기반, episode의 title을 가져온다.
        :param text: table>tbody>tr의 정보가 온다.(str)
        :return: td.title의 text를 가져온다
        """
        return text.select_one("img").attrs.get("alt")  # img에 alt로 붙은 제목 가져오기
    # return a.select_one("td.title").text.strip() # title td에서 뽑기

    def rating(self, text):
        """
        text로 받은 주소를 기반, episode의 rating을 가져온다.
        :param text: table>tbody>tr의 정보가 온다.(str)
        :return: td>div.rating_type>strong의 텍스트를 가져온다
        """
        return float(text.select_one("div.rating_type > strong").text)

    def date_(self, text):
        """
        text로 받은 주소를 기반, episode의 date를 가져온다.
        :param text: 
        :return: 
        """
        return text.select_one("td.num").text

    def crawling_all_episode(self):
        """
        주소를 기반으로 웹페이지 파싱 시작.
        1. status_code를 이용하여 끝 페이지 인식
        2. td의 첫 a에서 herf주소를 참조
           no=102 식의 첫번째 페이지의 첫 데이터의 attr를 참조해서 계산
           이 함수는 2번의 식으로 구현해보겠다
        :return: self.episodes에 모든 리스트를 추가   
        """
        dom = BeautifulSoup(self.response.text, "lxml")
        data = dom.find("table").find_all("tr", recursive=False)

        pattern = re.compile(r"no=(\d*)")
        self.episode_num = int(pattern.findall(data[0].select_one("a").attrs.get("href"))[0])

        for n in range(1, (self.episode_num // 10) + 2):
            self.__params["page"] = n
            self.response = requests.get(self.base_url, self.__params)
            dom = BeautifulSoup(self.response.text, "lxml")
            data = dom.find("table").find_all("tr", recursive=False)
            for item in data:
                self.episodes.append(Episode(
                    self.thumnail(item), self.title(item),
                    self.rating(item), self.date_(item)))
                # print(self.__params)
            # print(n)
            # self.page += 1

    def crawling_episode_images(self, no=1):
        """
        에피소드의 번호를 입력받아서 해당 에피소드의 이미지를 저장
        :param no: 에피소드 번호
        :return: 이미지 리스트를 리턴, 이미지가 없을 경우 none을 리턴
        """
        if self.episode_num:
            self.crawling_all_episode()

        # while (no < 0 or no > self.episode_num):
        #     no = int(input("Enter the Episode number : "))

        local_params = {
                'titleId': self.webtoonID,
                'no': no,
                }

        self.response = requests.get(self.base_detail_url, local_params)
        dom = BeautifulSoup(self.response.text, "lxml")
        images = dom.select_one("div.wt_viewer").select("img")

        image_list = []
        for i in images:
            image_list.append(i.attrs.get("src"))
        return image_list



    """
    1.
        1-1. 전체 에피소드 리스트를 가져오기 ok
        1-2. 에피소드 번호를 입력하면(no) 내부의 웹툰 이미지 주소를 가져오기 (여러장의 이미지로 분할되어있음) ok
        1-3. 썸네일이미지 또는 내부 웹툰 이미지를 저장 --> 403에러 -> 이런...
        1-4. 모든것을 통합해서 실행하면 웹툰을 각 화별 폴더를 생성해서 저장하기
        1-5. 저장한 파일을 접근할 수 있는 HTML생성 --> 뭔말이지??
    """


class Episode:
    # url_thumbnail, title, rating, date는 property로 구현 (전부 읽기전용, private으로 선언하지 말 것)
    def __init__(self, url_thumbnail, title, rating, date):
        self._url_thumbnail = url_thumbnail
        self._title = title
        self._rating = rating
        self._date = date

    @property
    def url_thumbnail(self):
        return self._url_thumbnail

    @property
    def title(self):
        return self._title

    @property
    def rating(self):
        return self._rating

    @property
    def date(self):
        return self._date


a = NaverWebtoonCrawler(654774, 1)
a.crawling_all_episode()
a.print_episodes()
print(a.crawling_episode_images(102))



