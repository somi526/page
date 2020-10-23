import sys
import time
import multiprocessing as mp
import re
import fire
import json
import re
import pathlib
import unicodedata
from bs4 import BeautifulSoup
from .google_drive import update_page
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DATA_PATH = pathlib.Path().absolute() / 'data'

def get_problems(*, original=None, to_html=None, min_level = None, max_level= None, chapter = None, student = None):
    with open(f"{DATA_PATH}/problems.json", 'r') as f:
        problems = json.load(f)
    if chapter:
        problems = list(filter(lambda problem: problem['chapter'] == chapter, problems))
    if min_level:
        problems = list(filter(lambda problem: problem['level'] >= min_level, problems))
    if max_level:
        problems = list(filter(lambda problem: problem['level'] <= max_level, problems))
    if student:
        problems = list(filter(lambda problem: problem not in student['solved'], problems))
    
    if original:
        bs = BeautifulSoup(open("teaching_teacher.html", 'r'), "html.parser")

        problems = []
        for a_question in bs.find_all("a", href=re.compile('.*acmicpc.*')):
            p_question = a_question.find_parent('p')
            if not p_question:
                continue
            id_match = re.match("BJ_(\d+)", unicodedata.normalize('NFKD', p_question.text))
            if not id_match:
                continue

            print(id_match.group(1))
            for p_answer in p_question.next_siblings:
                span_answer = p_answer.find("span")
                if "ff000" not in span_answer.attrs.get("style"):
                    break
                # if span_answer.decompose()
    elif to_html:
        html = ""
        for chapter in range(1, 11):
            html += f"<h1>{chapter}</h1>"
            for problem in filter(lambda problem : problem['chapter'] == chapter, problems):
                html += "<br>"
                html += problem['link']
                html += "<br>"
                if 'python' in problem:
                    html += '<br>'.join(problem["python"])
        return html
    else:
        return problems

def update_problems(*, update_page = None, update_level = None):
    if update_level:
        with mp.Pool(16) as pool:
            levels = pool.map(get_problems_level, range(1, 31))
        problems = [problem for level in levels for problem in level]
    else:
        with open(f"{DATA_PATH}/problems.json", 'r') as f:
            problems = json.load(f)

    if update_page:
        update_page('1B8J_rQtCihzPVSN5wOf7SgEOQRlJFs5Rsf3wFH9_hwM', 'teaching_teacher')
        for problem in problems:
            problem['chapter'] = -1
            problem['title'] = ""
            problem['type'] = ""
            problem['link'] = ""

        with open(f'{DATA_PATH}/algorithm.md') as f:
            cur_problem, cur_chapter = {}, ''
            for line in f.read().split('\n'):
                chapter_match = re.search(r'##.*\[(\d+)\].*', line)
                prob_match = re.search(r'(BJE?)_(\d+) (.*) \((.*)\)', line)
                eop_match = re.search(r'^\s*(#|\*|\[|<|Q)', line)
                reading_line = False
                if chapter_match:
                    cur_chapter = chapter_match.group(1)
                elif cur_chapter != "" and prob_match:
                    pid = prob_match.group(2)
                    cur_problem = next(filter(lambda problem: problem['id'] == pid, problems))
                    cur_problem['type'] = prob_match.group(1)
                    cur_problem['chapter'] = int(cur_chapter)
                    cur_problem['title'] = prob_match.group(3)
                    cur_problem['link'] = f'<a href="http://acmicpc.net/problem/{pid}">{prob_match.group(3)} ({cur_problem["level"]})</a>'
                    cur_problem['python'] = []
                    reading_line = True
                elif eop_match:
                    reading_line = False
                elif reading_line:
                    print(line)
                    if line != '':
                        cur_problem['python'].append(line)

    with open(f"{DATA_PATH}/problems.json", 'w') as f:
        json.dump(problems, f, ensure_ascii=False)

def get_problems_level(level):
    problems = []
    chrome_options = Options()
    chrome_options.add_argument('headless')  
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    try:
        level_problems = []
        for page in range(1, 100):
            driver.get(f"https://solved.ac/problems/level/{level}?sort=id&direction=asc&page={page}")
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'contents')))
            lines = driver.find_element_by_class_name('contents').text
            if '해당하는 문제가 없습니다' in lines:
                break
            for line in lines.split('\n'):
                level_problems.extend(re.findall(r'^ (\d+)', line))
        for problem in level_problems:
            problems.append({'id' : problem, 'level' : level})
    except Exception:
        driver.quit()
    else:
        driver.quit()
    return problems


if __name__ == "__main__":
    fire.Fire()