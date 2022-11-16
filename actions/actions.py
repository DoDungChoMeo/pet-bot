# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate(
    './actions/dodungchomeo-firebase-adminsdk-xziw5-7f7551a4b1.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()


def get_categories():
    docs = db.collection(u'categories').stream()
    categories = []
    for doc in docs:
        categories.append(doc.to_dict())
    return categories


def get_brands():
    docs = db.collection(u'brands').stream()
    brands = []
    for doc in docs:
        brands.append(doc.to_dict())
    return brands


def get_products_from_category(category_str, limit=10):
    docs = db.collection(u'products').where(
        u'categories', u'array_contains', category_str).limit(limit).stream()
    products = []
    for doc in docs:
        products.append(doc.to_dict())

    return products


def get_products_from_brand(brand_str, limit=5):
    docs = db.collection(u'products').where(
        u'brand', u'==', brand_str).limit(limit).stream()
    products = []
    for doc in docs:
        products.append(doc.to_dict())

    return products


# Hành động lấy danh mục sản phẩm ra từ database
class ActionCategories(Action):

    def name(self) -> Text:
        return "action_categories"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        textCategories = "Danh mục sản phẩm hiện có của shop\n"
        replies = []
        for category in get_categories():
            textCategories += "- {}\n".format(category['value'])
            replies.append({
                "content_type": "text",
                "title": category['value'],
                "payload": category['value'],
            })
        textCategories += "Bạn muốn xem sản phẩm thuộc danh mục nào?"


        message = {
            "text": textCategories,
            "quick_replies": replies
        }

        dispatcher.utter_message(json_message=message)

        return []

# Hành động lấy sản phẩm từ danh mục đã chọn ra từ database


class ActionGetProductsFromCategory(Action):

    def name(self) -> Text:
        return "action_get_products_from_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        chosen_category = next(
            tracker.get_latest_entity_values('category'), None)
        chosen_category = chosen_category.capitalize()       
        products = get_products_from_category(chosen_category, limit=5)

        newProducts = []
        for product in products:
            newProducts.append({
                "title": product["title"],
                "image_url": product["images"][0],
                "subtitle": f'{"{:,}".format(product["inventory"]["price"])} đồng',
                "default_action": {
                    "type": 'web_url',
                    "url": f"https://dodungchomeo.web.app/product/{product['bookmarkName']}",
                    "webview_height_ratio": "tall"
                },
                "buttons": [
                    {
                        "type": "web_url",
                        "url": f"https://dodungchomeo.web.app/product/{product['bookmarkName']}",
                        "title": "Xem chi tiết"
                    }
                ]
            })

        message = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": newProducts
                }
            }
        }

        dispatcher.utter_message(json_message=message)

        return []


# Hành động lấy danh sách nhãn hiệu ra từ database
class ActionBrands(Action):

    def name(self) -> Text:
        return "action_brands"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        textBrands = "Danh sách nhãn nhiệu mà shop đang bán\n"
        replies = []
        for brand in get_brands():
            textBrands += "- {}\n".format(brand['value'])
            replies.append({
                "content_type": "text",
                "title": brand['value'],
                "payload": brand['value'],
            })
        textBrands += "Bạn muốn xem sản phẩm thuộc nhãn hiệu nào?"

        message = {
            "text": textBrands,
            "quick_replies": replies
        }

        dispatcher.utter_message(json_message=message)

        return []


# Hành động lấy sản phẩm từ nhãn hàng
class ActionGetProductsFromBrand(Action):

    def name(self) -> Text:
        return "action_get_products_from_brand"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # chosen_brand = next(
        #     tracker.get_latest_entity_values('brand'), None)
        # products = get_products_from_brand(chosen_brand, limit=10)
        # print(products, chosen_brand)
        # newProducts = []
        # for product in products:
        #     newProducts.append({
        #         "title": product["title"],
        #         "image_url": product["images"][0],
        #         "subtitle": f'{"{:,}".format(product["inventory"]["price"])} đồng',
        #         "default_action": {
        #             "type": 'web_url',
        #             "url": f"https://dodungchomeo.web.app/product/{product['bookmarkName']}",
        #             "webview_height_ratio": "tall"
        #         },
        #         "buttons": [
        #             {
        #                 "type": "web_url",
        #                 "url": f"https://dodungchomeo.web.app/product/{product['bookmarkName']}",
        #                 "title": "Xem chi tiết"
        #             }
        #         ]
        #     })

        # message = {
        #     "attachment": {
        #         "type": "template",
        #         "payload": {
        #             "template_type": "generic",
        #             "elements": newProducts
        #         }
        #     }
        # }

        # dispatcher.utter_message(json_message=message)
        dispatcher.utter_message(text="get product from brand")

        return []


# Hành động tìm kiếm sản phẩm trong database
class ActionSearch(Action):

    def name(self) -> Text:
        return "action_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Chức năng tìm kiếm sản phẩm")

        return []
