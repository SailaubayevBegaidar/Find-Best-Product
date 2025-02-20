from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app import mongo
from datetime import datetime, timedelta

def hash_password(password):
    return generate_password_hash(password)

def check_password(hashed_password, password):
    return check_password_hash(hashed_password, password)

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            if identity.get('role') != 'admin':
                return jsonify(message='Admins only!'), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def compare_prices(product_name, category=None, time_range=None):
    query = {
        "name": {"$regex": product_name, "$options": "i"}
    }
    
    if category:
        query["category"] = category
        
    if time_range:
        query["last_updated"] = {
            "$gte": datetime.utcnow() - timedelta(days=time_range)
        }

    products = list(mongo.db.products.find(query).sort("price", 1))
    
    if not products:
        return None
        
    best_deal = products[0]
    price_differences = []
    
    for product in products[1:]:
        difference = {
            "source": product["source"],
            "price_difference": product["price"] - best_deal["price"],
            "percentage_difference": ((product["price"] - best_deal["price"]) / best_deal["price"]) * 100
        }
        price_differences.append(difference)
    
    return {
        "best_deal": best_deal,
        "price_differences": price_differences,
        "total_compared": len(products),
        "price_range": {
            "lowest": best_deal["price"],
            "highest": products[-1]["price"] if len(products) > 1 else best_deal["price"]
        }
    }
