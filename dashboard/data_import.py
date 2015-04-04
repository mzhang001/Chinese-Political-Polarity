__author__ = 'mengzhang'

import os,sys
import time
import csv
from urllib import request
from dashboard.models import User, Question, Answer
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import transaction

option_map = {
    "强烈同意": 0,  # Strong agreement
    "同意": 1,  # Agreement
    "反对": 2,  # Disagreement
    "强烈反对": 3,  # Strong disagreement
}

file_path = "dashboard/data/2014data.csv"
question_list = {}

def populate_question_list():
    f = open(file_path)
    line = f.readline()
    items = line.split(",")
    for i in items:
        if i not in ['序号', '参与时间', 'IP 地址', '性别', '出生年份', '年收入', '学历\n']:
            question_list[i] = Question(desc=i)
    f.close()

def parse():
    f = open(file_path)
    entry_list = []
    try:
        reader = csv.DictReader(f)
        for i in reader:
            entry_list.append(i)
    finally:
        f.close()
    return entry_list

@transaction.atomic
def run():
    populate_question_list()
    for i in question_list:
        question_list[i].save()
    entry_list = parse()
    for i in entry_list:
        user_args = {}
        user_args["uid"] = i["序号"]
        sys.stdout.write("\r%s" % i["序号"])
        sys.stdout.flush()
        user_args["is_male"] = (i["性别"] == "M")
        user_args["ip_address"] = i["IP 地址"]
        user_args["birth_year"] = i["出生年份"] if i["出生年份"] != "" else None
        user_args["income"] = i["年收入"] if i["年收入"] != "" else None
        user_args["education_background"] = i["学历"]
        try:
            t = i["参与时间"]
            if t and t != 'NULL':
                time.strptime(t, "%Y-%m-%d %H:%M:%S")
                user_args['time_created'] = t
        except ValueError:
            pass
        # print(user_args)
        user = User(**user_args)
        user.save()
        for j in i:
            if j not in ['序号', '参与时间', 'IP 地址', '性别', '出生年份', '年收入', '学历']:
                answer = Answer(
                    question = question_list[j],
                    user = user,
                    answer = option_map[i[j]]
                )
                answer.save()
