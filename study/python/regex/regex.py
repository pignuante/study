import re
story = """
Born to the prestigious Crownguards, the paragon family of Demacian service, Luxanna was destined for greatness. She grew up as the family's only daughter, and she immediately took to the advanced education and lavish parties required of families as high profile as the Crownguards. As Lux matured, it became clear that she was extraordinarily gifted. She could play tricks that made people believe they had seen things that did not actually exist. She could also hide in plain sight. Somehow, she was able to reverse engineer arcane magical spells after seeing them cast only once. She was hailed as a prodigy, drawing the affections of the Demacian government, military, and citizens alike.

As one of the youngest women to be tested by the College of Magic, she was discovered to possess a unique command over the powers of light. The young Lux viewed this as a great gift, something for her to embrace and use in the name of good. Realizing her unique skills, the Demacian military recruited and trained her in covert operations. She quickly became renowned for her daring achievements; the most dangerous of which found her deep in the chambers of the Noxian High Command. She extracted valuable inside information about the Noxus-Ionian conflict, earning her great favor with Demacians and Ionians alike. However, reconnaissance and surveillance was not for her. A light of her people, Lux's true calling was the League of Legends, where she could follow in her brother's footsteps and unleash her gifts as an inspiration for all of Demacia.
"""

# 1. {m}패턴지정자를 사용해서 a로 시작하는 4글자 단어를 전부 찾는다.
pattern01 = re.compile(r"\ba\w{3}\b")
print("1 : {}".format(pattern01.findall(story)))


# 2. r로 끝나는 모든 단어를 찾는다.
pattern02 = re.compile(r"\w*r\b")
print("2 : {}".format(pattern02.findall(story)))


# 3. a,b,c,d,e중 아무 문자나 3번 연속으로 들어간 단어를 찾는다.
pattern03 = re.compile(r"\w*[abcde]{3}\w*")
print("3 : {}".format(pattern03.findall(story)))


# 4. re.sub를 사용해서 ,로 구분된 앞/뒤 단어에 대해 앞단어는 대문자화 시키고,
#    뒷단어는 대괄호로 감싼다. 이 과정에서,
#    각각의 앞/뒤에 before, after그룹 이름을 사용한다.

print("4 : ")
print(
    re.sub(
        r"(?P<before>\w+), (?P<after>\w+)",
        lambda s: "{b}, <{a}>".format(b=s.group("before").upper(), a=s.group("after")),
        story))
