from apscheduler.schedulers.background import BackgroundScheduler
from app import mongo
from app.models import Product, PriceHistory
from app.parsers.product_parser import scrape_product_data
from datetime import datetime
import logging

scheduler = BackgroundScheduler()

def update_prices():
    """Фоновая задача для обновления цен"""
    products = Product.find_all()
    for product in products:
        try:
            new_data = scrape_product_data(product['url'], str(product['_id']))
            if new_data and 'price' in new_data:
                # Сохраняем историю цен
                price_history = PriceHistory(
                    product_id=product['_id'],
                    price=new_data['price']
                )
                price_history.save()

                # Обновляем текущую цену продукта
                Product.update(product['_id'], {'price': new_data['price']})

                # Проверяем снижение цены для уведомлений
                check_price_drop(product, new_data['price'])
        except Exception as e:
            logging.error(f"Error updating price for product {product['_id']}: {e}")

# Запускаем задачу каждые 6 часов
scheduler.add_job(update_prices, 'interval', hours=6)
scheduler.start() 