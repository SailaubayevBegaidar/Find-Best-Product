from flask import Blueprint, request, jsonify, render_template
from app import mongo
from app.models import Product
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import admin_required, compare_prices
from bson import ObjectId, errors

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/products', methods=['GET'])
def get_products():
    products = Product.find_all()
    return jsonify(products)

@bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    try:
        data = request.get_json()
        if not all(k in data for k in ('name', 'price', 'source')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        product = Product(
            name=data['name'],
            price=data['price'],
            source=data['source'],
            category=data.get('category'),
            url=data.get('url')
        )
        result = product.save()
        return jsonify({
            'message': 'Product created successfully',
            'product_id': str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/products/<product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    try:
        product = Product.find_by_id(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        product['_id'] = str(product['_id'])
        return jsonify(product), 200
    except errors.InvalidId:
        return jsonify({'error': 'Invalid product ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/products/<product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        data = request.get_json()
        result = Product.update(product_id, data)
        if result.modified_count:
            return jsonify({'message': 'Product updated successfully'}), 200
        return jsonify({'error': 'Product not found'}), 404
    except errors.InvalidId:
        return jsonify({'error': 'Invalid product ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/products/<product_id>', methods=['DELETE'])
@admin_required()
def delete_product(product_id):
    try:
        result = Product.delete(product_id)
        if result.deleted_count:
            return jsonify({'message': 'Product deleted successfully'}), 200
        return jsonify({'error': 'Product not found'}), 404
    except errors.InvalidId:
        return jsonify({'error': 'Invalid product ID'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/compare', methods=['GET'])
def compare_page():
    return render_template('compare.html')

@bp.route('/api/products/compare', methods=['GET'])
@jwt_required()
def compare_products():
    try:
        product_name = request.args.get('name', '')
        category = request.args.get('category')
        time_range = request.args.get('time_range', type=int)
        
        if not product_name:
            return jsonify({'error': 'Product name is required'}), 400
            
        comparison_result = compare_prices(product_name, category, time_range)
        
        if not comparison_result:
            return jsonify({'error': 'No products found'}), 404
            
        return jsonify(comparison_result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
