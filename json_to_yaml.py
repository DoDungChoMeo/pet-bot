import yaml
import json 

with open("petmart_ask_answer_data.json", "r") as file:
  data = json.load(file)

def formatRasaData(jsonData):
  intents = []
  utter_intents = []
  i = 1
  for dialog in jsonData:

    # print(dialog['ask'])
    # print(dialog['answer'])
    intents.append({ "examples": dialog['ask'], "intent": f"ask/{i}"})
    i += 1
    # break
  print(intents)
  with open(r'petmart_ask_answer_data.yaml', 'w') as file:
    documents = yaml.dump(intents, file)


formatRasaData(data)





# dict_file = [{'sports' : ['soccer', 'football', 'basketball', 'cricket', 'hockey', 'table tennis']},
# {'countries' : ['Pakistan', 'USA', 'India', 'China', 'Germany', 'France', 'Spain']}]

# with open(r'store_file.yaml', 'w') as file:
#     documents = yaml.dump(dict_file, file)