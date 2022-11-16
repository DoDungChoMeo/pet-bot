from bs4 import BeautifulSoup
import requests

url = "https://www.petmart.vn/hoi-dap-thu-y-mien-phi"
page = requests.get(url, verify=False)
soup = BeautifulSoup(page.text, 'html.parser')

def get_comments(): 
  soup.find(class_='comment')
  comments = soup.find_all("li", class_='comment')
  return comments

def classify_comments(comments):
  ask_list = []
  ask_answer_list = []
  for i in comments:
    content = i.find_all(class_='comment-content')
    if len(content) == 1:
      ask_list.append(content)
    else:
      ask_answer_list.append(content)
  return ask_list, ask_answer_list

comments = get_comments()
[ask_list, ask_answer_list] = classify_comments(comments)

story_list = [] # item with len > 3
ask_answer_data = []
for item in ask_answer_list:
  # [ask, answer] = item
  if (len(item) > 2):
    story_list.append(item)
  else:
    [ask, answer] = item
    ask = ask.contents[0].string
    answer = answer.contents[0].string
    # print(f'ask: {ask} answer: {answer}')
    ask_answer_data.append({"ask": ask, "answer": answer})

print(ask_answer_data)


import json
 
# Serializing json
json_object = json.dumps(ask_answer_data)
 
# Writing to sample.json
with open("ask_answer_petmart.json", "w") as outfile:
    outfile.write(json_object)
# ask_data = []
# for item in ask_list:
#   ask_data.append((item[0].contents)[0].string)
# print(ask_data)

# import csv
# with open('ask_data.csv', 'w') as file:
#     writer = csv.writer(file)
#     writer.writerow(ask_data)
