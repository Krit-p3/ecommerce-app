from schema.order import CartItem
from database.user import Users
from database.order import Orders, OrderItems
from database.product import Products
from fastapi import HTTPException


def add_cart(user: str, item: CartItem):
    global carts
    if user in carts:
        cart_items = carts[user]
    else:
        cart_items = []

    for i in cart_items:
        if i["product_id"] == item.product_id:
            i["quantity"] += item.quantity
            break
    else:
        cart_items.append(item.dict())

    carts[user] = cart_items
    return carts[user]


def view_cart(user: str):
    global carts
    if user in carts:
        return carts[user]
    else:
        return []


def place_order(user: str, db):
    global carts
    if user not in carts:
        raise HTTPException(status_code=400, detail="Cart is empty")
    _user = db.query(Users).filter(Users.username == user).first()

    if not _user:
        raise HTTPException(status_code=400, detail="User not found")

    order_id = f"order_{db.query(Orders).count() + 1}"

    cart_items = carts.pop(user)

    order = Orders(order_id=order_id, username=user, total_amount=0)

    total_amount = 0
    order_items = []

    for item in cart_items:
        product = db.query(Products).filter(Products.id == item["product_id"]).first()
        if not product:
            raise HTTPException(
                status_code=400, detail=f"Product {item.product} not found"
            )
        if product.quantity < item["quantity"]:
            raise HTTPException(
                status_code=400, detail=f"Insufficient stock for {item.product}"
            )
        total_amount += product.price * item["quantity"]

        product.quantity -= item["quantity"]

        order_item = OrderItems(
            order_id=str(order_id),
            product_id=item["product_id"],
            quantity=item["quantity"],
        )
        order_items.append(order_item)

    order.total_amount += total_amount

    db.add(order)
    db.add_all(order_items)
    db.commit()

    return order_id, total_amount
