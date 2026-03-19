from . import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, nullable=False)
    status     = db.Column(db.String(50), default="pending")
    total      = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items      = db.relationship("OrderItem", backref="order", lazy=True)

    def to_dict(self):
        return {
            "id":         self.id,
            "user_id":    self.user_id,
            "status":     self.status,
            "total":      self.total,
            "created_at": self.created_at.isoformat(),
            "items":      [i.to_dict() for i in self.items]
        }

class OrderItem(db.Model):
    __tablename__ = "order_items"

    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity   = db.Column(db.Integer, nullable=False)
    price      = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "quantity":   self.quantity,
            "price":      self.price
        }
