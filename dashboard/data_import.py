__author__ = 'mengzhang'

import os
import time
import csv
from urllib import request
from dashboard.models import User, Question, Answer
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

file_path = "data/2014data.csv"
answers = []

option_map = {
    "强烈同意": 0,  # Strong agreement
    "同意": 1,  # Agreement
    "反对": 2,  # Disagreement
    "强烈反对": 3,  # Strong disagreement
}

directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    os.makedirs(directory)

# Download csv file from the website
if not os.path.isfile(file_path):
    request.urlretrieve('http://zuobiao.me/resources/2014data.csv', file_path)

with open(file_path, 'r') as csvfile:
    data_reader = csv.reader(csvfile, delimiter=',')
    # Store all questions into database
    questions = next(data_reader)
    questions = questions[3:-4]
    questions_model = []
    for question in questions:
        q_db = Question(desc=question)
        q_db.save()
        questions_model.append(q_db)

    num_of_questions = len(questions)
    count = 0
    for row in data_reader:
        count += 1
        if count % 100 == 0:
            print(count)
        user_args = {
            "uid": int(row[0])
        }

        if row[-1]:
            user_args['education_background'] = row[-1]

        if row[2]:
            user_args['ip_address'] = row[2]

        if row[-2]:
            user_args['income'] = row[-2]

        if row[-3]:
            user_args['birth_year'] = int(row[-3])

        if row[-4] == 'M':
            user_args['is_male'] = True
        elif row[-4] == 'F':
            user_args['is_male'] = False

        try:
            t = row[1]
            if t and t != 'NULL':
                time.strptime(t, "%Y-%m-%d %H:%M:%S")
                user_args['time_created'] = t
        except ValueError:
            pass

        # try:
        user = User(**user_args)
        user.save()
        # except IntegrityError:
        # print(row)

        for i in range(3, len(row)-4):
            j = i - 3
            answer = Answer(
                question=questions_model[j],
                user=user,
                answer=option_map[row[i]]
            )
            answer.save()