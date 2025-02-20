from app import mongo
from bson import ObjectId
from datetime import datetime, timedelta

class Product:
    def __init__(self, name, price, source, category=None, url=None):
        self.name = name
        self.price = price
        self.source = source
        self.category = category
        self.url = url
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        return mongo.db.products.insert_one(self.__dict__)

    @staticmethod
    def find_all():
        return list(mongo.db.products.find())

    @staticmethod
    def find_by_id(product_id):
        try:
            return mongo.db.products.find_one({'_id': ObjectId(product_id)})
        except:
            return None

    @staticmethod
    def update(product_id, data):
        data['updated_at'] = datetime.utcnow()
        return mongo.db.products.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': data}
        )

    @staticmethod
    def delete(product_id):
        return mongo.db.products.delete_one({'_id': ObjectId(product_id)})

    @staticmethod
    def find_by_category(category):
        return mongo.db.products.find({"category": category})

    @staticmethod
    def find_best_price(product_name):
        return mongo.db.products.find({"name": {"$regex": product_name, "$options": "i"}}).sort("price", 1)

# Создание индексов
mongo.db.products.create_index([("name", 1)])
mongo.db.products.create_index([("category", 1)])
mongo.db.products.create_index([("price", 1)])

# Создание индексов для коллекций
def setup_indexes():
    # Products indexes
    mongo.db.products.create_index([("name", "text"), ("category", "text")])
    mongo.db.products.create_index([("price", 1)])
    mongo.db.products.create_index([("source", 1)])
    mongo.db.products.create_index([("created_at", -1)])

    # Users indexes
    mongo.db.users.create_index([("username", 1)], unique=True)
    mongo.db.users.create_index([("email", 1)], unique=True)

    # Price history indexes
    mongo.db.price_history.create_index([("product_id", 1)])
    mongo.db.price_history.create_index([("date", -1)])

class Collections:
    PRODUCTS = "products"
    USERS = "users"
    PRICE_HISTORY = "price_history"

class PriceHistory:
    def __init__(self, product_id, price, date=None):
        self.product_id = product_id
        self.price = price
        self.date = date or datetime.utcnow()

    def save(self):
        return mongo.db[Collections.PRICE_HISTORY].insert_one(self.__dict__)

    @staticmethod
    def get_history(product_id, days=30):
        start_date = datetime.utcnow() - timedelta(days=days)
        return list(mongo.db[Collections.PRICE_HISTORY].find(
            {"product_id": product_id, "date": {"$gte": start_date}}
        ).sort("date", -1))
