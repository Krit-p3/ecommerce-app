from fastapi import APIRouter, HTTPException
from schema.order import CartItem, Payment
from database.order import Orders
from lib import db_dependency, user_dependency
import asyncio
from sqlalchemy.orm import joinedload
from service import order

# In-memory cache
carts = {}


orders = APIRouter(prefix="/orders", tags=["orders"])


@orders.post("/add-to-cart")
async def add_to_cart(item: CartItem, user: user_dependency):
    # cart_key = user['username']

    # if cart_key in carts:
    #     cart_items  = carts[cart_key]
    # else:
    #     cart_items = []

    # check product already in cart or not
    # for i in cart_items:
    #     if i['product_id'] == item.product_id:
    #         i['quantity'] += item.quantity
    #         break
    # else:
    #     cart_items.append(item.dict())

    # update in-memory cart

    # carts[cart_key] = cart_items

    order.add_cart(user["username"], item)
    return {"message": f"Item added to cart for user {user['username']}"}


@orders.get("/view-cart")
async def view_cart(user: user_dependency):
    res = order.views_cart(user["username"])
    return res
    # cart_key = user['username']
    # if cart_key in carts:
    #     return carts[cart_key]
    # else:
    #     return []


# TODO: Fix here return amount is wrong
@orders.post("/place-order")
async def place_order(user: user_dependency, db: db_dependency):
    # cart_key = user['username']
    # if cart_key not in carts:
    #     raise HTTPException(status_code=400, detail="Cart is empty")

    # user = db.query(Users).filter(Users.username == cart_key).first()

    # if not user:
    #     raise HTTPException(status_code=400, detail="User not found")

    # order_id = f"order_{db.query(Orders).count() + 1}"

    # cart_items = carts.pop(cart_key)

    # order = Orders(
    #     order_id = str(order_id),
    #     username = str(cart_key),
    #     total_amount = 0
    # )

    # total_amount = 0
    # order_items = []
    # check stock avialiable

    # for item in cart_items:
    #     product = db.query(Products).filter(Products.id == item['product_id']).first()
    #     if not product:
    #         raise HTTPException(status_code=400, detail=f"Product {item.product} not found")
    #     if product.quantity < item['quantity']:
    #         raise HTTPException(status_code=400, detail=f"Insufficient stock for {item.product}")
    #     total_amount += product.price * item['quantity']

    # deduct stock
    #     product.quantity -= item['quantity']

    #     order_item = OrderItems(
    #         order_id = str(order_id),
    #         product_id= item["product_id"],
    #         quantity = item["quantity"]
    #     )
    #     order_items.append(order_item)

    # order.total_amount += total_amount

    # db.add(order)
    # db.add_all(order_items)
    # db.commit()
    order_id, total_amount = order.place_order(user["username"], db)
    return {"order_id": order_id, "total_amount": total_amount}


@orders.post("/confirm-payment")
async def confirm_payment(payment: Payment, user: user_dependency, db: db_dependency):
    order = db.query(Orders).filter(Orders.order_id == payment.order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")

    if order.username != user["username"]:
        raise HTTPException(
            status_code=403, detail="Not authorized to confirm this order"
        )

    # mock up payment processing time
    await asyncio.sleep(2)

    if order.total_amount != payment.amount:
        raise HTTPException(status_code=400, detail="Payment amount does not match")

    # will add confirm payment columns in Orders and confirm
    # db.commit()

    await notify_admin(order.order_id)
    await notify_user(order.order_id)

    return {"message": "Payment confirmed and order processed"}


@orders.get("/order-history")
async def get_order_history(user: user_dependency, db: db_dependency):
    orders = (
        db.query(Orders)
        .options(joinedload(Orders.items))
        .filter(Orders.username == user["username"])
        .all()
    )

    return orders


async def notify_admin(order_id: str):
    print(f"Admin notification: New Order {order_id} has been paid and processed")


async def notify_user(order_id: str):
    print(
        f"User notification: User Order {order_id} has been confirm and is being processed"
    )
