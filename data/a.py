from bs4 import BeautifulSoup
import itertools
import re
import unicodedata

bs = BeautifulSoup(open("teaching_teacher.html", 'r'), "html.parser")

problems = []
for a_question in bs.find_all("a", href=re.compile('.*acmicpc.*'), limit=10):
    p_question = a_question.find_parent('p')
    if not p_question:
        continue
    id_match = re.match("BJ_(\d+)",unicodedata.normalize('NFKD', p_question.text))
    if not id_match:
        continue

    print(id_match.group(1))
    for p_answer in p_question.next_siblings:
        span_answer = p_answer.find("span")
        if "ff000" not in span_answer.attrs.get("style"):
            break
        span_answer.decompose()
        #if span_answer.text:
        #    span_answer.



print(problems)