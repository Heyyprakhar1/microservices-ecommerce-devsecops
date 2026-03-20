from flask import Blueprint, request, jsonify, current_app
from . import db
from .models import Product
import jwt


product_bp = Blueprint("product", __name__)


def verify_token(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return None
    try:
        payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        return None


@product_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "product-service healthy"}), 200


@product_bp.route("/", methods=["GET"])
def get_products():
    category = request.args.get("category")
    if category:
        products = Product.query.filter_by(category=category).all()
    else:
        products = Product.query.all()
    return jsonify({"products": [p.to_dict() for p in products]}), 200


@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({"product": product.to_dict()}), 200


@product_bp.route("/", methods=["POST"])
def create_product():
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or not all(k in data for k in ("name", "price")):
        return jsonify({"error": "name and price required"}), 400

    product = Product(
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        stock=data.get("stock", 0),
        category=data.get("category")
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product created", "product": product.to_dict()}), 201


@product_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    product.name        = data.get("name", product.name)
    product.description = data.get("description", product.description)
    product.price       = data.get("price", product.price)
    product.stock       = data.get("stock", product.stock)
    product.category    = data.get("category", product.category)

    db.session.commit()
    return jsonify({"message": "Product updated", "product": product.to_dict()}), 200


@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200
