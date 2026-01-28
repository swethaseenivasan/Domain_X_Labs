import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="🛒 Creative Grocery Store", layout="wide")
st.title("🛒 Creative Grocery Store System")

# 1️⃣ Grocery inventory with categories, stock, price, image paths
grocery_items = {
    "Apple": {"price": 50, "stock": 10, "category": "Fruits 🥭", "image": "apple.png"},
    "Milk": {"price": 30, "stock": 5, "category": "Dairy 🥛", "image": "milk.png"},
    "Bread": {"price": 25, "stock": 8, "category": "Snacks 🍞", "image": "bread.png"},
    "Broccoli": {"price": 40, "stock": 6, "category": "Vegetables 🥦", "image": "broccoli.png"},
    "Cookies": {"price": 20, "stock": 15, "category": "Snacks 🍪", "image": "cookies.png"}
}

# 2️⃣ Initialize cart in session state
if "cart" not in st.session_state:
    st.session_state.cart = {}

# 3️⃣ Display items with images and stock color
st.subheader("Available Items:")
cols = st.columns(5)
for i, (item, info) in enumerate(grocery_items.items()):
    col = cols[i % 5]
    stock_color = "green"
    if info['stock'] == 0:
        stock_color = "red"
        stock_text = "❌ Out of stock"
    elif info['stock'] <= 3:
        stock_color = "orange"
        stock_text = f"⚠️ Low stock: {info['stock']}"
    else:
        stock_text = f"{info['stock']} in stock"

    # Display item with image (placeholder if images not present)
    col.markdown(f"**{item} - ₹{info['price']}**")
    col.markdown(f"<span style='color:{stock_color}'>{stock_text}</span>", unsafe_allow_html=True)

# 4️⃣ Select item and quantity
item_choice = st.selectbox("Select Item to Add to Cart", list(grocery_items.keys()))
quantity = st.number_input("Quantity", min_value=1, max_value=grocery_items[item_choice]['stock'])

# 5️⃣ Add to cart button
if st.button("Add to Cart"):
    if grocery_items[item_choice]['stock'] >= quantity:
        # Add/update cart
        if item_choice in st.session_state.cart:
            st.session_state.cart[item_choice]['quantity'] += quantity
        else:
            st.session_state.cart[item_choice] = {
                "price": grocery_items[item_choice]['price'],
                "quantity": quantity
            }
        # Reduce stock
        grocery_items[item_choice]['stock'] -= quantity
        fun_messages = ["🥳 You got this!", "🛍️ Shopping spree time!", "😎 Happy shopping!", "🍀 Lucky choice!"]
        st.success(f"✅ Added {quantity} x {item_choice} to cart! {random.choice(fun_messages)}")
    else:
        st.error("❌ Not enough stock!")

# 6️⃣ Show cart and allow removing items
if st.session_state.cart:
    st.subheader("🛒 Your Cart:")
    total = 0
    for item, info in st.session_state.cart.items():
        item_total = info['price'] * info['quantity']
        st.write(f"{item} - {info['quantity']} pcs - ₹{item_total}")
        total += item_total

    # 7️⃣ Apply discount if total > 200
    discount = 0
    if total > 200:
        discount = total * 0.05
        st.success(f"🎉 You got a 5% discount! -₹{discount:.2f}")
    total_after_discount = total - discount
    st.markdown(f"**Total: ₹{total_after_discount:.2f}**")

    # 8️⃣ Remove items option
    remove_item = st.selectbox("Remove Item from Cart", ["None"] + list(st.session_state.cart.keys()))
    if st.button("Remove Selected Item") and remove_item != "None":
        grocery_items[remove_item]['stock'] += st.session_state.cart[remove_item]['quantity']
        del st.session_state.cart[remove_item]
        st.warning(f"🗑️ Removed {remove_item} from cart.")

# 9️⃣ Checkout message
if st.button("Checkout") and st.session_state.cart:
    st.balloons()
    st.success(f"✅ Thank you for shopping! Your total bill is ₹{total_after_discount:.2f}")
    st.session_state.cart = {}

