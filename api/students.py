import sys
import time
import multiprocessing as mp
import re
import fire
import json
import re
import pathlib
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DATA_PATH = pathlib.Path().absolute() / 'data'

def get_students(*, to_html=None, name=None):
    with open(f"{DATA_PATH}/students.json", 'r') as f:
        students = json.load(f)
    if name:
        students = list(filter(lambda student: student['name'] == name, students))

    if to_html:
        with open(f"{DATA_PATH}/problems.json", 'r') as f:
            problems = json.load(f)
        html = ""
        for student in students:
            html += student['name']
            for prob_title in student['todo']:
                problem = next(filter(lambda prob: prob['id'] == prob_title, problems), "")
                html += problem['link'] + "<br>"
        return html

    return students

def update_student(student):
    chrome_options = Options()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    try:
        driver.get(f"https://www.acmicpc.net/user/{student['id']}")
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'panel-body')))
        student['solved'] = driver.find_element_by_class_name('panel-body').text.split()
    except Exception:
        driver.quit()
    else:
        driver.quit()
    return student

def update_students():
    with open(f"{DATA_PATH}/students.json", 'r') as f:
        students = json.load(f)
    with mp.Pool(16) as pool:
        students = pool.map(update_student, students)
    with open(f"{DATA_PATH}/students.json", 'w') as f:
        json.dump(students, f, ensure_ascii=False)

def update_todo():
    with open(f"{DATA_PATH}/students.json", 'r') as f:
        students = json.load(f)
    with open(f"{DATA_PATH}/problems.json", 'r') as f:
        problems = json.load(f)

    for student in students:
        print(student['name'])
        student['todo'] = [problem for problem in problems if problem['id'] not in student['solved'] and 'chapter' in problem]
        student['todo'].sort(key=lambda problem: (problem['chapter'], problem['level']))
        student['todo'] = [problem["id"] for problem in student['todo']]

    with open(f"{DATA_PATH}/students.json", 'w') as f:
        json.dump(students, f, ensure_ascii=False)


if __name__ == "__main__":
    fire.Fire()