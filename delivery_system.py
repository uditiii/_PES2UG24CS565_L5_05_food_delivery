"""Order queue manager for a food delivery kitchen.

Creates orders from a menu, moves them through delivery statuses, totals the
day's revenue and backs the queue up to disk as JSON.
"""
import json
from datetime import datetime

# Shared state. These containers are mutated in place (never rebound), so no
# `global` statements are needed.
orders = {}
menu = {}
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]
DEFAULT_MENU = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}

def create_order(customer, items, order_history=None):
    """Create an order and return its id.

    Raises ValueError for a missing customer, an empty order or a dish that
    is not on the menu (instead of silently charging a made-up price).
    """
    if not customer:
        raise ValueError("Customer name is required")
    if not items:
        raise ValueError("An order needs at least one item")
    unknown = [i for i in items if i not in menu]
    if unknown:
        raise ValueError("Not on the menu: " + ", ".join(unknown))
    total = sum(menu[i] for i in items)
    order_id = max(orders, default=0) + 1
    orders[order_id] = {"customer": customer, "items": items, "total": total, "status": "placed"}
    if order_history is not None:
        order_history.append(order_id)
    return order_id

def update_order_status(order_id, status):
    """Set an order's status; raise if the status or order id is invalid."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status!r}")
    if order_id not in orders:
        raise KeyError(f"Unknown order id: {order_id!r}")
    orders[order_id]["status"] = status

def read_menu_config(file="menu.json"):
    """Load the menu from a JSON file, falling back to the default menu."""
    try:
        with open(file, encoding="utf-8") as f:
            loaded = json.load(f)
    except (OSError, json.JSONDecodeError):
        loaded = DEFAULT_MENU
    menu.clear()
    menu.update(loaded)

def daily_revenue():
    """Return the total of all delivered orders."""
    return sum(o["total"] for o in orders.values() if o["status"] == "delivered")

def backup_orders(file="orders.json"):
    """Write all orders to a JSON file."""
    # JSON instead of pickle: no arbitrary code execution on load (B301/B403)
    with open(file, "w", encoding="utf-8") as f:
        json.dump(orders, f)

def restore_orders(file="orders.json"):
    """Replace the in-memory orders with the ones saved in a JSON file."""
    with open(file, encoding="utf-8") as f:
        # JSON object keys are always strings, so convert them back to ints
        restored = {int(k): v for k, v in json.load(f).items()}
    orders.clear()
    orders.update(restored)

def print_queue():
    """Print every order with its customer, status and total."""
    print(f"Order queue at {datetime.now()}")
    for order_id, order in orders.items():
        print(order_id, order["customer"], order["status"], order["total"])

def main():
    """Run a small demo of the order queue."""
    read_menu_config()
    history = []
    requests = [("Asha", ["pizza", "coke"]), ("Ravi", ["burger", "sushi"]), ("", [])]
    for customer, items in requests:
        try:
            create_order(customer, items, history)
        except ValueError as err:
            print("Could not create order:", err)
    updates = [(1, "delivered"), (2, "teleported"), (42, "delivered"), (3, "delivered")]
    for order_id, status in updates:
        try:
            update_order_status(order_id, status)
        except (ValueError, KeyError) as err:
            print("Could not update order:", err)
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    print_queue()

if __name__ == "__main__":
    main()
