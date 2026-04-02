# ============================================
# Restaurant Menu & Order Management System
# ============================================

# -------------------------------
# Given Data (unchanged)
# -------------------------------

menu = {
    "Paneer Tikka":   {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings":  {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":       {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":      {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":    {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":    {"category": "Mains",     "price": 40.0,  "available": True},
    "Gulab Jamun":    {"category": "Desserts",  "price": 90.0,  "available": True},
    "Rasgulla":       {"category": "Desserts",  "price": 80.0,  "available": True},
    "Ice Cream":      {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":   {"stock": 10, "reorder_level": 3},
    "Chicken Wings":  {"stock": 8, "reorder_level": 2},
    "Veg Soup":       {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka":      {"stock": 20, "reorder_level": 5},
    "Veg Biryani":    {"stock": 6, "reorder_level": 3},
    "Garlic Naan":    {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":    {"stock": 5, "reorder_level": 2},
    "Rasgulla":       {"stock": 4, "reorder_level": 3},
    "Ice Cream":      {"stock": 7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1, "items": ["Paneer Tikka", "Garlic Naan"], "total": 220.0},
        {"order_id": 2, "items": ["Gulab Jamun", "Veg Soup"], "total": 210.0},
        {"order_id": 3, "items": ["Butter Chicken", "Garlic Naan"], "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4, "items": ["Dal Tadka", "Garlic Naan"], "total": 220.0},
        {"order_id": 5, "items": ["Veg Biryani", "Gulab Jamun"], "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6, "items": ["Paneer Tikka", "Rasgulla"], "total": 260.0},
        {"order_id": 7, "items": ["Butter Chicken", "Veg Biryani"], "total": 570.0},
        {"order_id": 8, "items": ["Garlic Naan", "Gulab Jamun"], "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9, "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"], "total": 270.0},
    ],
}

# --------------------------------
# Task 1: Explore Menu
# --------------------------------

print("\nMenu by Category:\n")

categories = ["Starters", "Mains", "Desserts"]

for cat in categories:
    print(f"===== {cat} =====")
    for item, details in menu.items():
        if details["category"] == cat:
            status = "Available" if details["available"] else "Unavailable"
            print(f"{item:<15} ₹{details['price']:.2f}   [{status}]")
    print()

# basic stats
total_items = len(menu)
available_items = sum(1 for i in menu if menu[i]["available"])

# most expensive
exp_item = max(menu, key=lambda x: menu[x]["price"])

# items under 150
cheap_items = []
for item, d in menu.items():
    if d["price"] < 150:
        cheap_items.append((item, d["price"]))

print("Total items:", total_items)
print("Available items:", available_items)
print("Most expensive:", exp_item, menu[exp_item]["price"])
print("Items under 150:", cheap_items)


# --------------------------------
# Task 2: Cart Operations
# --------------------------------

cart = []

def add_item(name, qty):
    if name not in menu:
        print("Item not found in menu")
        return

    if not menu[name]["available"]:
        print("Item is currently unavailable")
        return

    # check if already in cart
    for c in cart:
        if c["item"] == name:
            c["quantity"] += qty
            print(f"Updated {name} quantity to {c['quantity']}")
            return

    cart.append({
        "item": name,
        "quantity": qty,
        "price": menu[name]["price"]
    })
    print(f"Added {name} x{qty}")


def remove_item(name):
    for c in cart:
        if c["item"] == name:
            cart.remove(c)
            print(f"Removed {name}")
            return
    print("Item not in cart")


def show_cart():
    print("\nCurrent Cart:")
    for c in cart:
        print(c)
    print()


# simulation
add_item("Paneer Tikka", 2)
show_cart()

add_item("Gulab Jamun", 1)
show_cart()

add_item("Paneer Tikka", 1)
show_cart()

add_item("Mystery Burger", 1)
add_item("Chicken Wings", 1)

remove_item("Gulab Jamun")
show_cart()

# final bill
print("\n========== Order Summary ==========")
subtotal = 0

for c in cart:
    total = c["quantity"] * c["price"]
    subtotal += total
    print(f"{c['item']:<18} x{c['quantity']}   ₹{total:.2f}")

gst = subtotal * 0.05
total_pay = subtotal + gst

print("------------------------------------")
print(f"Subtotal:           ₹{subtotal:.2f}")
print(f"GST (5%):           ₹{gst:.2f}")
print(f"Total Payable:      ₹{total_pay:.2f}")
print("====================================")


# --------------------------------
# Task 3: Inventory Tracker
# --------------------------------

import copy

inventory_backup = copy.deepcopy(inventory)

# test deep copy
inventory["Paneer Tikka"]["stock"] = 5

print("\nCheck Deep Copy:")
print("Inventory:", inventory["Paneer Tikka"])
print("Backup:", inventory_backup["Paneer Tikka"])

# restore
inventory = copy.deepcopy(inventory_backup)

# deduct stock based on cart
for c in cart:
    item = c["item"]
    qty = c["quantity"]

    if inventory[item]["stock"] >= qty:
        inventory[item]["stock"] -= qty
    else:
        print(f"Not enough stock for {item}")
        inventory[item]["stock"] = 0

# reorder alerts
print("\nReorder Alerts:")
for item, d in inventory.items():
    if d["stock"] <= d["reorder_level"]:
        print(f"⚠ {item} low stock: {d['stock']} left")

print("\nFinal Inventory vs Backup:")
print(inventory)
print(inventory_backup)


# --------------------------------
# Task 4: Sales Analysis
# --------------------------------

print("\nRevenue per day:")

def print_revenue(data):
    best_day = ""
    best_val = 0

    for day, orders in data.items():
        total = sum(o["total"] for o in orders)
        print(day, "->", total)

        if total > best_val:
            best_val = total
            best_day = day

    print("Best day:", best_day, best_val)


print_revenue(sales_log)

# most ordered item
item_count = {}

for orders in sales_log.values():
    for o in orders:
        for item in o["items"]:
            item_count[item] = item_count.get(item, 0) + 1

most_ordered = max(item_count, key=item_count.get)
print("Most ordered item:", most_ordered)

# add new day
sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"], "total": 260.0},
]

print("\nAfter adding new day:")
print_revenue(sales_log)

# numbered orders
print("\nAll Orders:")
all_orders = []

for date, orders in sales_log.items():
    for o in orders:
        all_orders.append((date, o))

for i, (date, o) in enumerate(all_orders, start=1):
    items_str = ", ".join(o["items"])
    print(f"{i}. [{date}] Order #{o['order_id']} — ₹{o['total']} — Items: {items_str}")
