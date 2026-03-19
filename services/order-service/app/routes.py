from flask import Blueprint, request, jsonify, current_app
from . import db
from .models import Order, OrderItem
import jwt

order_bp = Blueprint("order", __name__)

def verify_token(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return None
    try:
        payload = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        return None

@order_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "order-service healthy"}), 200

@order_bp.route("/", methods=["POST"])
def create_order():
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or "items" not in data:
        return jsonify({"error": "items required"}), 400

    total = sum(i["price"] * i["quantity"] for i in data["items"])

    order = Order(user_id=user["user_id"], total=total)
    db.session.add(order)
    db.session.flush()

    for item in data["items"]:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price=item["price"]
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify({"message": "Order placed", "order": order.to_dict()}), 201

@order_bp.route("/", methods=["GET"])
def get_orders():
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    orders = Order.query.filter_by(user_id=user["user_id"]).all()
    return jsonify({"orders": [o.to_dict() for o in orders]}), 200

@order_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    order = Order.query.filter_by(id=order_id, user_id=user["user_id"]).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify({"order": order.to_dict()}), 200

@order_bp.route("/<int:order_id>/status", methods=["PUT"])
def update_status(order_id):
    user = verify_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    data = request.get_json()
    order.status = data.get("status", order.status)
    db.session.commit()
    return jsonify({"message": "Status updated", "order": order.to_dict()}), 200
