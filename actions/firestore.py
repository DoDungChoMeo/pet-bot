# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# # Use a service account.
# cred = credentials.Certificate('./actions/dodungchomeo-firebase-adminsdk-xziw5-7f7551a4b1.json')

# app = firebase_admin.initialize_app(cred)

# db = firestore.client()

# def get_categories():
#   docs = db.collection(u'categories').stream()
#   categories = []
#   for doc in docs:
#       categories.append(doc.to_dict())
#   return categories

# def get_products_from_category(category_str, limit=10):
#   docs = db.collection(u'products').where(u'categories', u'array_contains', category_str).limit(limit).stream()
#   products = []
#   for doc in docs:
#       products.append(doc.to_dict())
#   return products

# # def get_products_from_category(category_str, limit=10):
# #     docs = db.collection(u'products').where(
# #         u'categories', u'array_contains', 'đồ dùng cho chó').limit(limit).stream()
# #     products = []
# #     for doc in docs:
# #         products.append(doc.to_dict())


# #     print(products)
# #     return products

# # print(get_products_from_category('đồ dùng cho chó'))

# def get_brands():
#   docs = db.collection(u'brands').stream()
#   brands = []
#   for doc in docs:
#       brands.append(doc.to_dict())
#   return brands

# def get_products_from_brand(brand_str, limit=10):
#     docs = db.collection(u'products').where(
#         u'brand', u'==', brand_str).limit(limit).stream()
#     products = []
#     for doc in docs:
#         products.append(doc.to_dict())

#     return products

# print(get_products_from_brand("CIAO"))