import yaml
import json

with open("petmart_ask_answer_data.json", "r", encoding='utf-8') as file:
  data = json.load(file)

def write_to_yaml(jsonData):
  intents = []
  utter_intents = []
  i = 1
  for dialog in jsonData:

    # print(dialog['ask'])
    # print(dialog['answer'])
    intents.append({ "examples": dialog['ask'], "antent": f"pet_faq/{i}"})
    utter_intents.append({ f"utter_pet_faq/{i}": {"text": dialog['answer']}})
    i += 1
    if i == 10:
      break
  
  with open(r'petmart_faq_intents.yaml', 'w', encoding="utf-8") as file:
    documents = yaml.dump(intents, file)

  with open(r'petmart_faq_utter_intents.yaml', 'w') as file:
    documents = yaml.dump(utter_intents, file)


write_to_yaml(data)





# dict_file = [{'sports' : ['soccer', 'football', 'basketball', 'cricket', 'hockey', 'table tennis']},
# {'countries' : ['Pakistan', 'USA', 'India', 'China', 'Germany', 'France', 'Spain']}]

# with open(r'store_file.yaml', 'w') as file:
#     documents = yaml.dump(dict_file, file)