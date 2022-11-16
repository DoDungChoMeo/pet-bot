def write_to_json_file(data, file_name):
  import json
  json_object = json.dumps(data)
  with open(file_name, "x") as outfile:
    outfile.write(json_object)

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


# list only have ask but haven't answer yet
ask_data = []
for item in ask_list:
  ask = (item[0].contents)[0].text
  ask_data.append({"ask": ask})

write_to_json_file(ask_data, "petmart_only_ask_data.json")


ask_answer_data = []
story_list = [] # item with len > 2
for item in ask_answer_list:
  # [ask, answer] = item
  if (len(item) > 2):
    story_list.append(item)
  else:
    [ask, answer] = item
    ask = ask.contents[0].text
    answer = answer.contents[0].text
    ask_answer_data.append({"ask": ask, "answer": answer})

write_to_json_file(ask_answer_data, "petmart_ask_answer_data.json")


stories_data = []
for story in story_list:
  i = 0
  story_data = []
  for item in story:
    if i % 2 == 0:
      ask = item.contents[0].text
      story_data.append({"ask": ask})
    else:
      answer = item.contents[0].text
      story_data.append({"answer": answer})
    i += 1
  stories_data.append(story_data)
print(len(stories_data))
write_to_json_file(stories_data, "petmart_stories_data.json")
