import re


class Node(object):
    """
        HTML태그 하나를 가지는 클래스
        내부에 다른 클래스를 가질수도 있음
        가장 큰 범위는 <html></html>
    """
    _pattern_tag_base = r'<{tag}.*?>\s*([.\w\W]*?)\s*</{tag}>'
    # tag를 기준으로 source를 나누는 regex
    _pattern_tag_content = r'<[^!]*?>([.\w\W]*)</.*?>'
    # tag안의 text를 뽑는 함수
    _pattern_class = r"<[^!]*?\s+?class\s*?=\s*?[\'\"]([.\w\W]*?)[\'\"]"
    # class의 이름만 뽑는 함수


    def __init__(self, source):  # Node class의 생성자. 이것은 source를 파라메터로 받는다.
        self.source = source

    def __str__(self):  # 함수를 print로 출력할떄 __str__를 호출한다.
        return '{}\n{}'.format(
            super().__str__(),  # 부모의 __str__메시지에 자신의 메시지를 추가.
            self.source
        )

    def find_tag(self, tag):
        pattern = re.compile(self._pattern_tag_base.format(tag=tag))
        # tag를 기반으로 html을 분할한다
        m_list = re.finditer(pattern, self.source)
        # finditer로 패턴에 맞는 것들을 iterator로 m_list에 넣는다.
        if m_list:
            return_list = [Node(m.group()) for m in m_list]
            # m_list에 들어간 패턴에 매칭된 그룹들을 return_list에 넣는다
            return return_list if len(return_list) > 1 else return_list[0]
            # 검색결과가 다수일때는 list, 1개일때는 Node객체를 return.
        return None

    @property
    def content(self):
        """
        Node인스턴스의 내용을 리턴
        :return: Node(태그)내부의 내용 문자열을 리턴
        """
        # _pattern_tag_content = r'<[^!]*?>([.\w\W]*)</.*?>'
        pattern = re.compile(self._pattern_tag_content)  # pattern을 content용으로
        m = re.search(pattern, self.source.strip())  # 패턴에 맞는 문자열을 찾는다
        if m:  # 패턴에 맞는 문자열이 존재 할시,
            return m.group(1).strip()  # 그룹에 매팅된 문자열을 반환한다
        # group()함수는 pattern에서 그룹이 존재 할시, 그 그룹의 숫자에 맞는 index를 반환한다
        # 단, group(0)은 문자열 전체를 의미한다
        return None

    @property
    def class_(self):
        """
        해당 Node가 가진 class속성의 value를 리턴 (문자열)
        :return:
        """
        pattern = re.compile(self._pattern_class)
        results = pattern.finditer(self.source)  # findall로 하면 편하지만 굳이 iter를 사용해봤다.
        if results:
            # 더 간단하게 할수있지만 굳이 lambda를 사용하였다...
            result = list(map(lambda x: x.group(1) if not " " in x.group(1) else x.group(1).split(), results))
            # 한 class안에 여러개가 존재하면, 2중 list로 표현하였다.
            return result
        return None


with open('./example.html') as f:
    html = Node(f.read())

print(html.class_)

