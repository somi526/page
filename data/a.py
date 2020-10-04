from html import unescape
from html.parser import HTMLParser
with open("teaching_teacher.html", 'r') as f:
    a = f.read()
    p = HTMLParser()
    #p.feed(a)
    print(unescape(a))
    print(dir(p))
    #print(a[-50000:].encode().decode())