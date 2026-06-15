"""
pages/1_Support_Chatbot.py – MiniStore Support Chatbot (standalone, no data.py)
"""

import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MiniStore Support",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Product catalogue (mirrored from app.py) ───────────────────────────────────
PRODUCTS = [
    {"id": 1, "name": "Wireless Noise-Cancelling Headphones", "category": "Electronics", "price": 89.99, "emoji": "🎧", "description": "Premium over-ear headphones with 30-hour battery life and deep bass.", "rating": 4.8, "reviews": 1240},
    {"id": 2, "name": "Minimalist Leather Wallet", "category": "Accessories", "price": 34.99, "emoji": "👜", "description": "Slim RFID-blocking bifold wallet. Holds up to 8 cards and cash.", "rating": 4.6, "reviews": 875},
    {"id": 3, "name": "Stainless Steel Water Bottle", "category": "Home & Kitchen", "price": 24.95, "emoji": "🫙", "description": "Double-wall insulated 32 oz bottle keeps drinks cold 24h / hot 12h.", "rating": 4.7, "reviews": 2103},
    {"id": 4, "name": "Running Shoes – UltraBoost", "category": "Sports", "price": 119.00, "emoji": "👟", "description": "Lightweight mesh upper with responsive cushioning for long-distance runs.", "rating": 4.9, "reviews": 3412},
    {"id": 5, "name": "Portable Bluetooth Speaker", "category": "Electronics", "price": 49.99, "emoji": "🔊", "description": "360° surround sound, IPX7 waterproof, 12-hour playtime.", "rating": 4.5, "reviews": 987},
    {"id": 6, "name": "Organic Green Tea Set", "category": "Food & Drinks", "price": 19.99, "emoji": "🍵", "description": "Hand-picked Japanese matcha & sencha tea collection, 40 premium bags.", "rating": 4.7, "reviews": 654},
    {"id": 7, "name": "Smart LED Desk Lamp", "category": "Home & Kitchen", "price": 39.95, "emoji": "💡", "description": "Touch-dimmer, USB-C charging port, 5 colour temperatures.", "rating": 4.6, "reviews": 519},
    {"id": 8, "name": "Yoga Mat – Pro Grip", "category": "Sports", "price": 29.99, "emoji": "🧘", "description": "Non-slip natural rubber mat, 6mm thick, includes carrying strap.", "rating": 4.8, "reviews": 1788},
    {"id": 9, "name": "Polarised Sunglasses", "category": "Accessories", "price": 54.00, "emoji": "🕶️", "description": "UV400 polarised lenses in a lightweight titanium frame.", "rating": 4.5, "reviews": 432},
]

ALL_CATEGORIES = sorted({p["category"] for p in PRODUCTS})

# ── Rule-based chatbot engine ──────────────────────────────────────────────────

def _build_product_response(query):
    q = query.lower()
    # Match a specific product by name keywords
    for p in PRODUCTS:
        if any(word in q for word in p["name"].lower().split() if len(word) > 3):
            stars = "⭐" * int(p["rating"])
            return (
                f"{p['emoji']} **{p['name']}**\n\n"
                f"- **Category:** {p['category']}\n"
                f"- **Price:** ${p['price']:.2f}\n"
                f"- **Rating:** {stars} {p['rating']} ({p['reviews']:,} reviews)\n"
                f"- **Description:** {p['description']}\n\n"
                f"Would you like to know about shipping, returns, or payment options for this item?"
            )
    # Match a category
    for cat in ALL_CATEGORIES:
        if cat.lower() in q:
            items = [p for p in PRODUCTS if p["category"] == cat]
            lines = "\n".join(f"- {p['emoji']} **{p['name']}** – ${p['price']:.2f}" for p in items)
            return f"🛍️ **{cat} products:**\n\n{lines}\n\nAsk me about any of these for more details!"
    # Full catalogue
    lines = "\n".join(f"- {p['emoji']} **{p['name']}** ({p['category']}) – ${p['price']:.2f}" for p in PRODUCTS)
    return f"🛍️ **Our full product catalogue:**\n\n{lines}\n\nAsk me about any product for details!"


def get_bot_response(message):
    msg = message.lower()
    tokens = set(msg.split())

    # ── Greetings ──
    if tokens & {"hi", "hello", "hey", "hiya", "howdy"}:
        return (
            "👋 **Hello! Welcome to MiniStore Support!**\n\n"
            "I can help you with:\n"
            "- 🛍️ Product information\n"
            "- 🚚 Delivery & shipping\n"
            "- 💰 Refunds\n"
            "- 📦 Returns & exchanges\n"
            "- 💳 Payment methods\n"
            "- 📋 Order status\n\n"
            "What can I help you with today?"
        )

    # ── Products ──
    if tokens & {"product", "products", "item", "items", "catalogue", "catalog", "sell", "available", "show", "list", "headphones", "wallet", "bottle", "shoes", "speaker", "tea", "lamp", "mat", "sunglasses"}:
        return _build_product_response(message)

    # ── Delivery / Shipping ──
    if tokens & {"delivery", "deliver", "shipping", "ship", "arrive", "arrival", "dispatch", "track", "tracking", "days"}:
        return (
            "🚚 **Shipping & Delivery**\n\n"
            "- **Standard shipping** (3–5 business days) – FREE on orders over $50, otherwise $4.99\n"
            "- **Express shipping** (1–2 business days) – $9.99\n"
            "- **Same-day delivery** available in select cities for orders placed before 12 PM\n\n"
            "Once your order ships you'll receive a tracking link via email within 24 hours. "
            "Need help tracking an existing order? Share your order number!"
        )

    # ── Refunds ──
    if tokens & {"refund", "refunds", "reimbursement", "reimburse", "overcharged", "charge"}:
        return (
            "💰 **Refund Policy**\n\n"
            "We offer a **30-day full refund** on all products – no questions asked.\n\n"
            "**How to request a refund:**\n"
            "1. Email **refunds@ministore.com** with your order number\n"
            "2. Our team processes the request within 1–2 business days\n"
            "3. Funds appear in your account within **5–7 business days**\n\n"
            "Refunds are issued to the original payment method. Which order would you like to refund?"
        )

    # ── Returns ──
    if tokens & {"return", "returns", "exchange", "swap", "damaged", "broken", "defective"}:
        return (
            "📦 **Returns & Exchanges**\n\n"
            "Our hassle-free return window is **30 days** from the delivery date.\n\n"
            "**Return process:**\n"
            "1. Visit **ministore.com/returns** or share your order number here\n"
            "2. Print the prepaid return label we email you (FREE for defective items, $3.99 otherwise)\n"
            "3. Drop the parcel at any post office\n"
            "4. Receive your replacement or refund within **5–7 business days**\n\n"
            "Damaged or defective items are always returned at our cost. 🙂"
        )

    # ── Payment ──
    if tokens & {"payment", "pay", "paying", "card", "credit", "debit", "paypal", "visa", "mastercard", "amex", "klarna", "instalment", "installment"}:
        return (
            "💳 **Payment Methods**\n\n"
            "MiniStore accepts:\n\n"
            "- **Credit & Debit cards** – Visa, Mastercard, American Express, Discover\n"
            "- **PayPal** (including Pay Later)\n"
            "- **Apple Pay** & **Google Pay**\n"
            "- **Klarna** – split into 4 interest-free instalments\n"
            "- **MiniStore Gift Cards**\n\n"
            "All transactions are secured with **256-bit SSL encryption**. 🔒"
        )

    # ── Order status ──
    if tokens & {"order", "orders", "status", "purchase", "confirm", "confirmation", "invoice", "number"}:
        return (
            "📋 **Order Status**\n\n"
            "To check your order:\n\n"
            "1. **Email** – check for a confirmation from **orders@ministore.com**\n"
            "2. **Account page** – log in at ministore.com → *My Orders*\n"
            "3. **Chat** – share your **order number** (format: MS-XXXXXX) and I'll look it up\n\n"
            "**Typical timeline:**\n"
            "✅ Confirmed → 📦 Processing (1 day) → 🚚 Shipped → 🏠 Delivered\n\n"
            "What's your order number?"
        )

    # ── Thanks ──
    if tokens & {"thanks", "thank", "ty", "cheers", "great", "perfect", "awesome"}:
        return "😊 You're welcome! Is there anything else I can help you with?"

    # ── Contact / Human agent ──
    if tokens & {"agent", "human", "person", "contact", "email", "phone", "call", "representative"}:
        return (
            "📞 **Contact MiniStore Support**\n\n"
            "- **Email:** support@ministore.com (reply within 2 hours)\n"
            "- **Phone:** 1-800-MINI-STORE (Mon–Fri, 9 AM – 6 PM ET)\n"
            "- **Live chat:** Available Mon–Sun 8 AM – 10 PM ET\n\n"
            "Type **'talk to agent'** to be connected to a human right away."
        )

    # ── Fallback ──
    return (
        "🤔 I'm not sure I understood that. Here's what I can help with:\n\n"
        "- 🛍️ **Products** – try *'show products'* or a product name\n"
        "- 🚚 **Delivery** – try *'shipping info'*\n"
        "- 💰 **Refunds** – try *'refund policy'*\n"
        "- 📦 **Returns** – try *'how to return'*\n"
        "- 💳 **Payments** – try *'payment methods'*\n"
        "- 📋 **Order status** – try *'track my order'*\n\n"
        "Or type **'contact support'** to speak with a human agent."
    )


# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.chat-header {
    background: linear-gradient(135deg, #6C63FF 0%, #3B82F6 100%);
    border-radius: 16px; padding: 28px 36px; color: white;
    margin-bottom: 24px; display: flex; align-items: center; gap: 20px;
}
.chat-header-icon { font-size: 3rem; }
.chat-header h2   { margin: 0 0 4px; font-size: 1.7rem; font-weight: 700; }
.chat-header p    { margin: 0; opacity: 0.88; font-size: 0.95rem; }

.status-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #ECFDF5; color: #059669; border: 1px solid #A7F3D0;
    border-radius: 50px; padding: 4px 12px; font-size: 0.78rem;
    font-weight: 600; margin-bottom: 8px;
}
.status-dot {
    width: 7px; height: 7px; background: #10B981;
    border-radius: 50%; animation: pulse 1.5s infinite;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

.back-link a {
    color: #6C63FF !important; font-size: 0.88rem;
    font-weight: 500; text-decoration: none !important;
}
.back-link a:hover { text-decoration: underline !important; }

#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "greeted" not in st.session_state:
    st.session_state.greeted = False

# ── Header ────────────────────────────────────────────────────────────────────
col_back, _ = st.columns([1, 5])
with col_back:
    st.markdown('<div class="back-link"><a href="/" target="_self">← Back to Store</a></div>', unsafe_allow_html=True)

st.markdown("""
<div class="chat-header">
    <div class="chat-header-icon">🤖</div>
    <div>
        <h2>MiniStore Support</h2>
        <p>Ask me about products, delivery, refunds, returns, payments, or order status.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="status-badge"><div class="status-dot"></div> Support Bot Online</div>', unsafe_allow_html=True)

# ── Quick-action buttons ───────────────────────────────────────────────────────
QUICK_ACTIONS = [
    "🛍️ Show all products",
    "🚚 Shipping info",
    "💰 Refund policy",
    "📦 How to return",
    "💳 Payment methods",
    "📋 Track my order",
]

st.markdown("**Quick actions:**")
qa_cols = st.columns(len(QUICK_ACTIONS))
for col, label in zip(qa_cols, QUICK_ACTIONS):
    with col:
        if st.button(label, use_container_width=True, key=f"qa_{label}"):
            st.session_state.chat_history.append({"role": "user", "content": label})
            st.session_state.chat_history.append({"role": "assistant", "content": get_bot_response(label)})
            st.rerun()

st.divider()

# ── Auto-greeting ──────────────────────────────────────────────────────────────
if not st.session_state.greeted:
    st.session_state.chat_history.append({"role": "assistant", "content": get_bot_response("hello")})
    st.session_state.greeted = True

# ── Chat history ───────────────────────────────────────────────────────────────
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# ── Chat input ─────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Type your question here…"):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    reply = get_bot_response(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(reply)

# ── Clear chat ─────────────────────────────────────────────────────────────────
if st.session_state.chat_history:
    if st.button("🗑️ Clear conversation", type="secondary"):
        st.session_state.chat_history = []
        st.session_state.greeted = False
        st.rerun()
        