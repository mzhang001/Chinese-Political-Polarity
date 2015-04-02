__author__ = 'mengzhang'

import os
import csv
from urllib import request


file_path = "data/2014data.csv"
answers = []

directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    os.makedirs(directory)

# Download csv file from the website
if not os.path.isfile(file_path):
    request.urlretrieve('http://zuobiao.me/resources/2014data.csv', file_path)


#
option_map = {
    "强烈同意": 0,  # Strong agreement
    "同意": 1,  # Agreement
    "反对": 2,  # Disagreement
    "强烈反对": 3,  # Strong disagreement
}

# option_map = {
#     "强烈同意": "Strong agreement",  # Strong agreement
#     "同意": "Agreement",  # Agreement
#     "反对": "Disagreement",  # Disagreement
#     "强烈反对": "Strong disagreement",  # Strong disagreement
# }

education_option_map = {
}

with open(file_path, 'r') as csvfile:
    data_reader = csv.reader(csvfile, delimiter=',')
    questions = next(data_reader)
    questions = questions[3:-4]
    num_of_questions = len(questions)
    for row in data_reader:
        options = []
        for i in range(3, len(row)-4):
            options.append(option_map[row[i]])
        options.append(row[53])
        if row[54]:
            options.append(int(row[54]))
        options.append(row[55])
        options.append(row[56])
        answers.append(options)

distribution = {}

for question in questions:
    # distribution[question] = {
    #     option_map["强烈同意"]: 0,
    #     option_map["同意"]: 0,
    #     option_map["反对"]: 0,
    #     option_map["强烈反对"]: 0
    # }
    distribution[question] = [0, 0, 0, 0]

for ans in answers:
    for i in range(num_of_questions):
        # if ans[i] not in distribution[questions[i]]:
        #     distribution[questions[i]][ans[i]] = 0
        distribution[questions[i]][ans[i]] += 1

print(distribution)


