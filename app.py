"""
Retail Billing and Inventory System - Web Application
Built with Streamlit for seamless deployment and real-time interaction.
Corporate Aesthetic: Deep Navy Blue (#1E3A8A), Slate Gray (#64748B), Crisp White (#FFFFFF), Emerald (#059669).
"""

import datetime
import html
import io
import math
import os
import pandas as pd
import streamlit as st

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
PAGE_TITLE = "Apex Retail | Billing & Inventory System"
PAGE_ICON = "🛒"
TAX_RATE = 0.05  # 5% Tax rate as per original project specification
INVENTORY_FILE = "inventory.txt"
STORE_NAME = "APEX RETAIL MART PVT. LTD."
STORE_TAGLINE = "Your Trusted Neighborhood Supermarket"
STORE_GSTIN = "29AAAAA0000A1Z5"
STORE_ADDRESS = "42 MG Road, Commercial Plaza, Tech City, Bangalore - 560001"
STORE_PHONE = "+91 98765 43210"
STORE_EMAIL = "billing@apexretail.in"

# Set Streamlit Page Config
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# PROFESSIONAL CORPORATE CSS STYLING
# ==============================================================================
st.markdown("""
<style>
    /* Global Fonts & Palette */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Main background & container */
    .main {
        background-color: #F8FAFC;
    }

    /* Primary Navy Header Bar */
    .top-header-banner {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F2356 100%);
        padding: 24px 32px;
        border-radius: 12px;
        color: #FFFFFF;
        box-shadow: 0 4px 14px 0 rgba(15, 35, 86, 0.15);
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }

    .top-header-banner h1 {
        color: #FFFFFF !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
    }

    .top-header-banner p {
        color: #93C5FD !important;
        font-size: 13px !important;
        margin: 4px 0 0 0 !important;
    }

    .header-badge {
        background-color: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
        color: #FFFFFF;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* KPI Stat Cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px 22px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.08);
        border-color: #CBD5E1;
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        color: #1E3A8A;
        letter-spacing: -0.5px;
    }
    .kpi-sub {
        font-size: 11px;
        color: #94A3B8;
        margin-top: 4px;
    }

    /* Section Cards */
    .content-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        margin-bottom: 24px;
    }

    .card-title {
        font-size: 17px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 10px;
    }

    /* Status Badges */
    .badge-in-stock {
        background-color: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-low-stock {
        background-color: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-out-stock {
        background-color: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        display: inline-block;
    }

    /* Summary Financial Totals Box */
    .bill-summary-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 20px;
        margin-top: 16px;
    }
    .bill-summary-row {
        display: flex;
        justify-content: space-between;
        font-size: 14px;
        color: #475569;
        padding: 6px 0;
    }
    .bill-summary-total {
        display: flex;
        justify-content: space-between;
        font-size: 19px;
        font-weight: 800;
        color: #1E3A8A;
        border-top: 2px dashed #CBD5E1;
        padding-top: 12px;
        margin-top: 8px;
    }

    /* Real Tax Invoice Receipt Layout */
    .invoice-container {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        padding: 36px 40px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        max-width: 680px;
        margin: 0 auto;
        color: #1E293B;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    .invoice-header-title {
        font-size: 20px;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    .invoice-store-subtitle {
        text-align: center;
        font-size: 11px;
        color: #64748B;
        line-height: 1.5;
        margin-bottom: 14px;
    }
    .invoice-divider {
        border-top: 1px dashed #94A3B8;
        margin: 14px 0;
    }
    .invoice-meta-table {
        width: 100%;
        font-size: 12px;
        line-height: 1.6;
        margin-bottom: 12px;
    }
    .invoice-meta-table td {
        vertical-align: top;
    }
    .invoice-item-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
        margin: 16px 0;
    }
    .invoice-item-table th {
        background-color: #F1F5F9;
        color: #334155;
        font-weight: 700;
        text-align: left;
        padding: 8px 10px;
        border-top: 1px solid #CBD5E1;
        border-bottom: 1px solid #CBD5E1;
        font-size: 11px;
        text-transform: uppercase;
    }
    .invoice-item-table td {
        padding: 9px 10px;
        border-bottom: 1px solid #F1F5F9;
        color: #1E293B;
    }
    .invoice-item-table tr:last-child td {
        border-bottom: 1px solid #CBD5E1;
    }
    .invoice-total-row {
        display: flex;
        justify-content: flex-end;
        gap: 32px;
        font-size: 12px;
        padding: 3px 0;
    }
    .invoice-grand-total {
        font-size: 15px;
        font-weight: 800;
        color: #0F172A;
        border-top: 1px solid #1E293B;
        border-bottom: 1px solid #1E293B;
        padding: 6px 0;
        margin-top: 6px;
    }
    .invoice-footer {
        text-align: center;
        font-size: 11px;
        color: #64748B;
        margin-top: 24px;
        padding-top: 12px;
        border-top: 1px dashed #CBD5E1;
    }

    /* Print styling */
    @media print {
        body * {
            visibility: hidden;
        }
        .invoice-container, .invoice-container * {
            visibility: visible;
        }
        .invoice-container {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }
        header, .stSidebar, .stButton, [data-testid="stSidebar"] {
            display: none !important;
        }
    }

    /* Buttons Corporate Styling */
    div.stButton > button:first-child {
        border-radius: 8px;
        font-weight: 600;
        padding: 8px 20px;
        transition: all 0.2s ease;
    }
    
    /* Primary buttons */
    div.stButton > button[kind="primary"] {
        background-color: #1E3A8A;
        border-color: #1E3A8A;
        color: #FFFFFF;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1E40AF;
        border-color: #1E40AF;
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.25);
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# NUMBER TO INDIAN RUPEE WORDS HELPER
# ==============================================================================
def number_to_words(n):
    """Converts a floating-point number into Indian currency words for professional invoices."""
    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
             "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    def convert_below_thousand(num):
        result = ""
        if num >= 100:
            result += units[num // 100] + " Hundred "
            num %= 100
        if 1 <= num <= 19:
            result += units[num] + " "
        elif num >= 20:
            result += tens[num // 10] + (" " + units[num % 10] if num % 10 != 0 else "") + " "
        return result.strip()

    rupees = int(math.floor(n))
    paise = int(round((n - rupees) * 100))

    if rupees == 0 and paise == 0:
        return "Zero Rupees Only"

    parts = []
    # Crores
    crores = rupees // 10000000
    if crores > 0:
        parts.append(convert_below_thousand(crores) + " Crore")
        rupees %= 10000000
    # Lakhs
    lakhs = rupees // 100000
    if lakhs > 0:
        parts.append(convert_below_thousand(lakhs) + " Lakh")
        rupees %= 100000
    # Thousands
    thousands = rupees // 1000
    if thousands > 0:
        parts.append(convert_below_thousand(thousands) + " Thousand")
        rupees %= 1000
    # Remaining hundreds
    if rupees > 0:
        parts.append(convert_below_thousand(rupees))

    rupee_str = " ".join(parts).strip() + " Rupees" if parts else ""
    paise_str = (convert_below_thousand(paise) + " Paise") if paise > 0 else ""

    if rupee_str and paise_str:
        return f"{rupee_str} and {paise_str} Only"
    elif rupee_str:
        return f"{rupee_str} Only"
    else:
        return f"{paise_str} Only"


# ==============================================================================
# INVENTORY FILE STORAGE (PRESERVES ORIGINAL SPEC)
# ==============================================================================
def get_starter_inventory():
    """Returns the default product catalog including original starter items."""
    return {
        "P101": {"name": "Rice (1kg)", "price": 60.0, "stock": 20},
        "P102": {"name": "Milk (1L)", "price": 30.0, "stock": 15},
        "P103": {"name": "Bread (Brown)", "price": 25.0, "stock": 12},
        "P104": {"name": "Sugar (1kg)", "price": 44.0, "stock": 25},
        "P105": {"name": "Wheat Flour (5kg)", "price": 210.0, "stock": 18},
        "P106": {"name": "Sunflower Oil (1L)", "price": 135.0, "stock": 14},
        "P107": {"name": "Assam Tea (250g)", "price": 95.0, "stock": 8},
        "P108": {"name": "Farm Eggs (Pack of 6)", "price": 48.0, "stock": 4},
        "P109": {"name": "Dark Chocolate (100g)", "price": 85.0, "stock": 30},
        "P110": {"name": "Organic Honey (500g)", "price": 220.0, "stock": 5}
    }


def load_inventory_from_file():
    """Read product details from inventory.txt file."""
    inventory = {}
    if not os.path.exists(INVENTORY_FILE):
        starter = get_starter_inventory()
        save_inventory_to_file(starter)
        return starter

    try:
        with open(INVENTORY_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    code = parts[0].strip().upper()
                    name = parts[1].strip()
                    price = float(parts[2].strip())
                    stock = int(parts[3].strip())
                    inventory[code] = {
                        "name": name,
                        "price": price,
                        "stock": stock
                    }
        if not inventory:
            inventory = get_starter_inventory()
            save_inventory_to_file(inventory)
    except Exception as e:
        inventory = get_starter_inventory()
        save_inventory_to_file(inventory)

    return inventory


def save_inventory_to_file(inventory):
    """Write product details to inventory.txt file."""
    try:
        with open(INVENTORY_FILE, "w") as file:
            for code, item in inventory.items():
                line = f"{code},{item['name']},{item['price']:.2f},{item['stock']}\n"
                file.write(line)
        return True
    except Exception as e:
        st.error(f"Error persisting inventory to file: {e}")
        return False


# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
if "inventory" not in st.session_state:
    st.session_state.inventory = load_inventory_from_file()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoices" not in st.session_state:
    st.session_state.invoices = []

if "current_invoice" not in st.session_state:
    st.session_state.current_invoice = None

if "invoice_counter" not in st.session_state:
    st.session_state.invoice_counter = 1001

if "customer_name" not in st.session_state:
    st.session_state.customer_name = "Walk-in Customer"

if "customer_phone" not in st.session_state:
    st.session_state.customer_phone = "9876543210"

if "payment_method" not in st.session_state:
    st.session_state.payment_method = "UPI / QR Code"


# ==============================================================================
# SIDEBAR NAVIGATION & SYSTEM CONTROLS
# ==============================================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 12px 0 18px 0; border-bottom: 1px solid #E2E8F0;">
        <div style="display: inline-flex; align-items: center; justify-content: center; width: 50px; height: 50px; background-color: #1E3A8A; color: white; border-radius: 12px; font-size: 24px; margin-bottom: 8px;">
            🛒
        </div>
        <div style="font-size: 18px; font-weight: 800; color: #1E3A8A; letter-spacing: -0.5px;">APEX RETAIL PRO</div>
        <div style="font-size: 12px; color: #64748B; font-weight: 500;">Retail Billing & Inventory Suite</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    selected_view = st.radio(
        "Navigation Menu",
        options=["📦 Product Catalog", "🧾 Billing & Checkout", "📊 Inventory Management", "📑 Invoice History"],
        index=1,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Quick System Analytics in Sidebar
    total_skus = len(st.session_state.inventory)
    total_items = sum(item["stock"] for item in st.session_state.inventory.values())
    low_stock_count = sum(1 for item in st.session_state.inventory.values() if item["stock"] <= 5)
    cart_items_count = sum(item["quantity"] for item in st.session_state.cart)

    st.markdown("<p style='font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase;'>Live System Metrics</p>", unsafe_allow_html=True)
    
    col_sb1, col_sb2 = st.columns(2)
    with col_sb1:
        st.metric("Total SKUs", total_skus)
        st.metric("Items in Stock", total_items)
    with col_sb2:
        st.metric("Low Stock (<5)", low_stock_count)
        st.metric("Active Cart", f"{cart_items_count} items")

    st.markdown("---")
    st.markdown("<p style='font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase;'>Data Maintenance</p>", unsafe_allow_html=True)

    if st.button("💾 Persist Inventory to File", use_container_width=True):
        if save_inventory_to_file(st.session_state.inventory):
            st.success("Saved to inventory.txt!")

    if st.button("🔄 Reset Demo Starter Data", use_container_width=True):
        st.session_state.inventory = get_starter_inventory()
        save_inventory_to_file(st.session_state.inventory)
        st.session_state.cart = []
        st.session_state.current_invoice = None
        st.success("Reset to official starter inventory!")
        st.rerun()

    st.markdown("""
    <div style="margin-top: 40px; padding: 12px; background: #F1F5F9; border-radius: 8px; font-size: 11px; color: #64748B; text-align: center;">
        <b>College Mini Project</b><br>
        Standard 5% Tax Billing Model<br>
        Cloud Ready Prototype
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# TOP APP HEADER
# ==============================================================================
st.markdown(f"""
<div class="top-header-banner">
    <div>
        <h1>{STORE_NAME}</h1>
        <p>Enterprise Point of Sale (POS) & Automated Inventory Tracking System</p>
    </div>
    <div style="display: flex; gap: 8px; flex-wrap: wrap;">
        <span class="header-badge">🏛️ GSTIN: {STORE_GSTIN}</span>
        <span class="header-badge">⚡ Tax Rate: 5% (SGST 2.5% + CGST 2.5%)</span>
        <span class="header-badge">🟢 Real-Time Synced</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# VIEW 1: PRODUCT CATALOG
# ==============================================================================
if selected_view == "📦 Product Catalog":
    st.markdown("### 📦 Warehouse & Product Catalog")
    st.caption("Browse available inventory, monitor live stock levels, and inspect product details.")

    # High-level Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Registered SKUs</div>
            <div class="kpi-value">{len(st.session_state.inventory)}</div>
            <div class="kpi-sub">Unique products in database</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        total_units = sum(i["stock"] for i in st.session_state.inventory.values())
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Warehouse Stock Level</div>
            <div class="kpi-value">{total_units:,}</div>
            <div class="kpi-sub">Total physical units available</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        total_val = sum(i["price"] * i["stock"] for i in st.session_state.inventory.values())
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Inventory Valuation</div>
            <div class="kpi-value">₹{total_val:,.2f}</div>
            <div class="kpi-sub">At current retail prices</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        low_count = sum(1 for i in st.session_state.inventory.values() if i["stock"] <= 5)
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Stock Replenishment Alerts</div>
            <div class="kpi-value" style="color: {'#B91C1C' if low_count > 0 else '#047857'};">{low_count}</div>
            <div class="kpi-sub">Items with ≤ 5 units left</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Search and Filter Toolbar
    c_search, c_filter = st.columns([3, 1])
    with c_search:
        search_query = st.text_input("🔍 Search Catalog", placeholder="Search by Product Code (e.g. P101) or Name (e.g. Rice)...")
    with c_filter:
        filter_status = st.selectbox("Stock Filter", ["All Items", "In Stock (>5 units)", "Low Stock (≤5 units)", "Out of Stock (0 units)"])

    # Prepare catalog data
    records = []
    for code, item in st.session_state.inventory.items():
        # Filtering logic
        if search_query:
            q = search_query.strip().lower()
            if q not in code.lower() and q not in item["name"].lower():
                continue

        if filter_status == "In Stock (>5 units)" and item["stock"] <= 5:
            continue
        elif filter_status == "Low Stock (≤5 units)" and (item["stock"] > 5 or item["stock"] == 0):
            continue
        elif filter_status == "Out of Stock (0 units)" and item["stock"] > 0:
            continue

        if item["stock"] == 0:
            badge = '<span class="badge-out-stock">Out of Stock (0)</span>'
            status_text = "Out of Stock"
        elif item["stock"] <= 5:
            badge = f'<span class="badge-low-stock">Low Stock ({item["stock"]} left)</span>'
            status_text = f"Low Stock ({item['stock']})"
        else:
            badge = f'<span class="badge-in-stock">Available ({item["stock"]})</span>'
            status_text = f"Healthy ({item['stock']})"

        records.append({
            "Code": code,
            "Product Name": item["name"],
            "Unit Price (₹)": f"₹{item['price']:.2f}",
            "Current Stock": item["stock"],
            "Status": status_text,
            "Inventory Value (₹)": f"₹{item['price'] * item['stock']:.2f}"
        })

    if records:
        df_catalog = pd.DataFrame(records)
        st.dataframe(
            df_catalog,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Code": st.column_config.TextColumn("Product Code", width="medium"),
                "Product Name": st.column_config.TextColumn("Product Description", width="large"),
                "Unit Price (₹)": st.column_config.TextColumn("Unit Price (₹)", width="medium"),
                "Current Stock": st.column_config.ProgressColumn(
                    "Stock Progress",
                    help="Live stock relative to typical stock ceiling (50 units)",
                    format="%d units",
                    min_value=0,
                    max_value=50,
                    width="medium"
                ),
                "Status": st.column_config.TextColumn("Stock Health Status", width="medium"),
                "Inventory Value (₹)": st.column_config.TextColumn("Total Asset Value", width="medium")
            }
        )

        st.markdown("<br>", unsafe_allow_html=True)
        # Quick Add Section from Catalog
        with st.expander("⚡ Quick Add Product Directly to Cart"):
            q_cols = st.columns([3, 2, 2])
            with q_cols[0]:
                selected_code = st.selectbox(
                    "Select Product",
                    options=list(st.session_state.inventory.keys()),
                    format_func=lambda c: f"{c} - {st.session_state.inventory[c]['name']} (₹{st.session_state.inventory[c]['price']:.2f}) [Stock: {st.session_state.inventory[c]['stock']}]"
                )
            prod = st.session_state.inventory[selected_code]
            max_qty = prod["stock"]
            with q_cols[1]:
                quick_qty = st.number_input("Quantity", min_value=1, max_value=max(1, max_qty), value=1, step=1, disabled=(max_qty <= 0))
            with q_cols[2]:
                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                if st.button("➕ Add to Active Bill", type="primary", disabled=(max_qty <= 0), use_container_width=True):
                    # Check current cart quantity
                    existing_in_cart = sum(item["quantity"] for item in st.session_state.cart if item["code"] == selected_code)
                    if existing_in_cart + quick_qty > prod["stock"]:
                        st.error(f"Cannot add: Only {prod['stock']} units in stock ({existing_in_cart} already in cart).")
                    else:
                        # Append or update cart
                        found = False
                        for item in st.session_state.cart:
                            if item["code"] == selected_code:
                                item["quantity"] += quick_qty
                                item["amount"] = item["quantity"] * item["price"]
                                found = True
                                break
                        if not found:
                            st.session_state.cart.append({
                                "code": selected_code,
                                "name": prod["name"],
                                "price": prod["price"],
                                "quantity": quick_qty,
                                "amount": quick_qty * prod["price"]
                            })
                        st.success(f"Added {quick_qty}x {prod['name']} to bill! Switch to 'Billing & Checkout' to complete order.")
                        st.rerun()
    else:
        st.info("No products match your current search or filter criteria.")


# ==============================================================================
# VIEW 2: BILLING & CHECKOUT
# ==============================================================================
elif selected_view == "🧾 Billing & Checkout":
    st.markdown("### 🧾 Point-of-Sale Billing & Checkout")
    st.caption("Select items, adjust quantities with real-time stock ceiling validation, and generate tax invoices.")

    col_billing_left, col_billing_right = st.columns([5, 6], gap="large")

    # LEFT COLUMN: PRODUCT SELECTION & CUSTOMER DETAILS
    with col_billing_left:
        st.markdown("""
        <div class="content-card">
            <div class="card-title">👤 Customer & Transaction Metadata</div>
        """, unsafe_allow_html=True)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.session_state.customer_name = st.text_input("Customer Name", value=st.session_state.customer_name)
        with col_c2:
            st.session_state.customer_phone = st.text_input("Mobile Number", value=st.session_state.customer_phone)

        st.session_state.payment_method = st.selectbox(
            "Payment Method",
            ["UPI / QR Code", "Cash", "Credit / Debit Card", "Net Banking"]
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # Product Selection Form
        st.markdown("""
        <div class="content-card">
            <div class="card-title">🛒 Add Products to Cart</div>
        """, unsafe_allow_html=True)

        # Build options for selector
        available_codes = list(st.session_state.inventory.keys())

        if available_codes:
            selected_product_code = st.selectbox(
                "Choose Product",
                options=available_codes,
                format_func=lambda c: f"[{c}] {st.session_state.inventory[c]['name']} - ₹{st.session_state.inventory[c]['price']:.2f} (Stock: {st.session_state.inventory[c]['stock']})"
            )

            current_prod = st.session_state.inventory[selected_product_code]
            cart_existing_qty = sum(item["quantity"] for item in st.session_state.cart if item["code"] == selected_product_code)
            available_for_cart = current_prod["stock"] - cart_existing_qty

            # Display product insight
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.caption("Unit Price")
                st.markdown(f"**₹{current_prod['price']:.2f}**")
            with col_info2:
                st.caption("Warehouse Stock")
                st.markdown(f"**{current_prod['stock']} units**")
            with col_info3:
                st.caption("Available to Add")
                if available_for_cart > 0:
                    st.markdown(f"<span style='color: #047857; font-weight: 700;'>{available_for_cart} units</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color: #B91C1C; font-weight: 700;'>0 units (Limit reached)</span>", unsafe_allow_html=True)

            # Quantity input with dynamic validation
            if available_for_cart > 0:
                quantity_to_add = st.number_input(
                    "Quantity to Add",
                    min_value=1,
                    max_value=available_for_cart,
                    value=1,
                    step=1
                )
                
                line_amount = quantity_to_add * current_prod["price"]
                st.info(f"Item Subtotal: **₹{line_amount:.2f}** ({quantity_to_add} × ₹{current_prod['price']:.2f})")

                if st.button("➕ Add Item to Bill", type="primary", use_container_width=True):
                    found = False
                    for item in st.session_state.cart:
                        if item["code"] == selected_product_code:
                            item["quantity"] += quantity_to_add
                            item["amount"] = item["quantity"] * item["price"]
                            found = True
                            break
                    if not found:
                        st.session_state.cart.append({
                            "code": selected_product_code,
                            "name": current_prod["name"],
                            "price": current_prod["price"],
                            "quantity": quantity_to_add,
                            "amount": line_amount
                        })
                    st.success(f"Added {quantity_to_add} × {current_prod['name']} to bill!")
                    st.rerun()
            else:
                st.warning("⚠️ Cannot add more units of this item. Stock exhausted or already fully allocated in active cart.")
        else:
            st.warning("No products available in inventory.")

        st.markdown("</div>", unsafe_allow_html=True)

    # RIGHT COLUMN: LIVE CART & TAX INVOICE CHECKOUT
    with col_billing_right:
        st.markdown("""
        <div class="content-card">
            <div class="card-title">🧾 Current Bill Summary & Invoice Cart</div>
        """, unsafe_allow_html=True)

        if st.session_state.cart:
            # Cart Table
            cart_rows = []
            for idx, item in enumerate(st.session_state.cart):
                cart_rows.append({
                    "Item #": idx + 1,
                    "Code": item["code"],
                    "Product": item["name"],
                    "Rate": f"₹{item['price']:.2f}",
                    "Qty": item["quantity"],
                    "Amount": f"₹{item['amount']:.2f}"
                })

            st.dataframe(
                pd.DataFrame(cart_rows),
                use_container_width=True,
                hide_index=True
            )

            # Option to remove items
            with st.expander("🗑️ Modify or Remove Cart Items"):
                col_rem_select, col_rem_btn = st.columns([3, 1])
                with col_rem_select:
                    remove_idx = st.selectbox(
                        "Select Item to Remove",
                        options=range(len(st.session_state.cart)),
                        format_func=lambda i: f"{st.session_state.cart[i]['name']} ({st.session_state.cart[i]['quantity']} units)"
                    )
                with col_rem_btn:
                    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
                    if st.button("Remove Item", use_container_width=True):
                        removed_item = st.session_state.cart.pop(remove_idx)
                        st.info(f"Removed {removed_item['name']} from cart.")
                        st.rerun()

            # FINANCIAL CALCULATIONS (5% TAX STRUCTURE)
            subtotal = sum(item["amount"] for item in st.session_state.cart)
            cgst = subtotal * (TAX_RATE / 2)  # 2.5%
            sgst = subtotal * (TAX_RATE / 2)  # 2.5%
            total_tax = subtotal * TAX_RATE   # 5%
            grand_total = subtotal + total_tax

            st.markdown(f"""
            <div class="bill-summary-box">
                <div class="bill-summary-row">
                    <span>Taxable Subtotal ({len(st.session_state.cart)} distinct products):</span>
                    <span style="font-weight: 600;">₹{subtotal:,.2f}</span>
                </div>
                <div class="bill-summary-row">
                    <span>Central GST (CGST @ 2.5%):</span>
                    <span>₹{cgst:,.2f}</span>
                </div>
                <div class="bill-summary-row">
                    <span>State GST (SGST @ 2.5%):</span>
                    <span>₹{sgst:,.2f}</span>
                </div>
                <div class="bill-summary-row" style="font-weight: 600; color: #047857;">
                    <span>Total Tax Liability (5%):</span>
                    <span>₹{total_tax:,.2f}</span>
                </div>
                <div class="bill-summary-total">
                    <span>NET PAYABLE AMOUNT:</span>
                    <span>₹{grand_total:,.2f}</span>
                </div>
                <div style="font-size: 11px; color: #64748B; margin-top: 8px; text-align: right;">
                    <i>{number_to_words(grand_total)}</i>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            col_btn_clear, col_btn_checkout = st.columns([1, 2])
            with col_btn_clear:
                if st.button("❌ Empty Cart", use_container_width=True):
                    st.session_state.cart = []
                    st.warning("Cart emptied.")
                    st.rerun()

            with col_btn_checkout:
                if st.button("✅ Process Checkout & Generate Tax Invoice", type="primary", use_container_width=True):
                    # Verify stock availability one final time
                    stock_error = False
                    for item in st.session_state.cart:
                        code = item["code"]
                        if st.session_state.inventory[code]["stock"] < item["quantity"]:
                            st.error(f"Insufficient stock for {item['name']}. Available: {st.session_state.inventory[code]['stock']}, In cart: {item['quantity']}.")
                            stock_error = True
                            break

                    if not stock_error:
                        # Deduct stock real-time
                        for item in st.session_state.cart:
                            code = item["code"]
                            st.session_state.inventory[code]["stock"] -= item["quantity"]

                        # Persist updated inventory to file
                        save_inventory_to_file(st.session_state.inventory)

                        # Generate unique invoice metadata
                        now = datetime.datetime.now()
                        invoice_id = f"INV-{now.strftime('%Y%m%d')}-{st.session_state.invoice_counter}"
                        st.session_state.invoice_counter += 1

                        invoice_record = {
                            "invoice_id": invoice_id,
                            "timestamp": now.strftime("%d-%b-%Y %I:%M:%S %p"),
                            "date": now.strftime("%d/%m/%Y"),
                            "time": now.strftime("%I:%M %p"),
                            "customer_name": st.session_state.customer_name or "Walk-in Customer",
                            "customer_phone": st.session_state.customer_phone or "N/A",
                            "payment_method": st.session_state.payment_method,
                            "items": list(st.session_state.cart),
                            "subtotal": subtotal,
                            "cgst": cgst,
                            "sgst": sgst,
                            "tax": total_tax,
                            "grand_total": grand_total,
                            "amount_words": number_to_words(grand_total)
                        }

                        # Store in session state
                        st.session_state.invoices.append(invoice_record)
                        st.session_state.current_invoice = invoice_record

                        # Clear active cart
                        st.session_state.cart = []

                        st.success("🎉 Transaction successfully completed! Stock deducted and invoice generated.")
                        st.balloons()
                        st.rerun()

        else:
            st.markdown("""
            <div style="text-align: center; padding: 48px 16px; color: #94A3B8;">
                <div style="font-size: 48px; margin-bottom: 12px;">🛒</div>
                <div style="font-size: 16px; font-weight: 600; color: #475569;">Cart is currently empty</div>
                <p style="font-size: 13px;">Select items from the catalog on the left to begin creating a retail tax bill.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================================================
    # DISPLAY LAST GENERATED TAX INVOICE (RECEIPT GENERATION REQUIREMENT)
    # ==========================================================================
    if st.session_state.current_invoice:
        st.markdown("---")
        st.markdown("### 🖨️ Retail Tax Invoice (Print Ready)")
        st.caption("Official tax compliant invoice generated for the most recent transaction.")

        inv = st.session_state.current_invoice

        # Build Invoice Table HTML
        items_html = ""
        for idx, itm in enumerate(inv["items"], start=1):
            items_html += f"""
            <tr>
                <td style="text-align: center;">{idx}</td>
                <td><b>{html.escape(itm['name'])}</b> <span style="color:#64748B; font-size:10px;">({itm['code']})</span></td>
                <td style="text-align: center;">{itm['quantity']}</td>
                <td style="text-align: right;">₹{itm['price']:.2f}</td>
                <td style="text-align: right;">₹{itm['amount']:.2f}</td>
            </tr>
            """

        invoice_rendered_html = f"""
        <div class="invoice-container">
            <div class="invoice-header-title">{STORE_NAME}</div>
            <div class="invoice-store-subtitle">
                {STORE_TAGLINE}<br>
                {STORE_ADDRESS}<br>
                <b>GSTIN:</b> {STORE_GSTIN} &nbsp;|&nbsp; <b>Ph:</b> {STORE_PHONE} &nbsp;|&nbsp; <b>Email:</b> {STORE_EMAIL}
            </div>

            <div class="invoice-divider"></div>

            <table class="invoice-meta-table">
                <tr>
                    <td style="width: 50%;">
                        <b>Invoice No:</b> {inv['invoice_id']}<br>
                        <b>Date & Time:</b> {inv['timestamp']}<br>
                        <b>POS Terminal:</b> POS-01 (Cashier: Staff Admin)
                    </td>
                    <td style="width: 50%; text-align: right;">
                        <b>Billed To:</b> {html.escape(inv['customer_name'])}<br>
                        <b>Contact:</b> {html.escape(inv['customer_phone'])}<br>
                        <b>Payment Mode:</b> <span style="color:#047857; font-weight:700;">{inv['payment_method']}</span>
                    </td>
                </tr>
            </table>

            <table class="invoice-item-table">
                <thead>
                    <tr>
                        <th style="width: 8%; text-align: center;">#</th>
                        <th style="width: 46%;">Item Description</th>
                        <th style="width: 14%; text-align: center;">Qty</th>
                        <th style="width: 16%; text-align: right;">Rate (₹)</th>
                        <th style="width: 16%; text-align: right;">Total (₹)</th>
                    </tr>
                </thead>
                <tbody>
                    {items_html}
                </tbody>
            </table>

            <div style="width: 100%; margin-top: 10px;">
                <div class="invoice-total-row">
                    <span style="color: #64748B;">Taxable Subtotal:</span>
                    <span style="width: 100px; text-align: right; font-weight: 600;">₹{inv['subtotal']:.2f}</span>
                </div>
                <div class="invoice-total-row">
                    <span style="color: #64748B;">CGST @ 2.5%:</span>
                    <span style="width: 100px; text-align: right;">₹{inv['cgst']:.2f}</span>
                </div>
                <div class="invoice-total-row">
                    <span style="color: #64748B;">SGST @ 2.5%:</span>
                    <span style="width: 100px; text-align: right;">₹{inv['sgst']:.2f}</span>
                </div>
                <div class="invoice-total-row invoice-grand-total">
                    <span>GRAND TOTAL (INCL. 5% TAX):</span>
                    <span style="width: 100px; text-align: right;">₹{inv['grand_total']:.2f}</span>
                </div>
            </div>

            <div style="margin-top: 12px; font-size: 11px; color: #475569; background: #F8FAFC; padding: 8px 12px; border-radius: 6px;">
                <b>Amount in Words:</b> {inv['amount_words']}
            </div>

            <div class="invoice-footer">
                Thank you for shopping with us! Please visit again.<br>
                <i>Goods once sold can be returned/exchanged within 7 days with this original receipt.</i><br>
                <span style="font-size: 9px; color: #94A3B8;">This is a computer-generated Tax Invoice and requires no physical signature.</span>
            </div>
        </div>
        """

        st.markdown(invoice_rendered_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Invoice Download / Print Actions
        c_act1, c_act2, c_act3 = st.columns([1, 1, 1])

        # Printable HTML file download
        full_html_document = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Tax Invoice - {inv['invoice_id']}</title>
<style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; margin: 0; padding: 20px; }}
    .invoice-container {{ background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px; padding: 32px 36px; max-width: 650px; margin: 0 auto; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }}
    .invoice-header-title {{ font-size: 20px; font-weight: 800; color: #1e3a8a; text-align: center; margin-bottom: 2px; }}
    .invoice-store-subtitle {{ text-align: center; font-size: 11px; color: #64748b; line-height: 1.5; margin-bottom: 14px; }}
    .invoice-divider {{ border-top: 1px dashed #94a3b8; margin: 12px 0; }}
    .invoice-meta-table {{ width: 100%; font-size: 12px; margin-bottom: 12px; }}
    .invoice-item-table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin: 16px 0; }}
    .invoice-item-table th {{ background: #f1f5f9; color: #334155; text-align: left; padding: 8px; border-top: 1px solid #cbd5e1; border-bottom: 1px solid #cbd5e1; font-size: 11px; }}
    .invoice-item-table td {{ padding: 8px; border-bottom: 1px solid #f1f5f9; }}
    .invoice-total-row {{ display: flex; justify-content: flex-end; gap: 32px; font-size: 12px; padding: 3px 0; }}
    .invoice-grand-total {{ font-size: 15px; font-weight: 800; color: #0f172a; border-top: 1px solid #0f172a; border-bottom: 1px solid #0f172a; padding: 6px 0; }}
    .invoice-footer {{ text-align: center; font-size: 11px; color: #64748b; margin-top: 20px; padding-top: 12px; border-top: 1px dashed #cbd5e1; }}
    @media print {{ body {{ background: #fff; padding: 0; }} .invoice-container {{ border: none; box-shadow: none; max-width: 100%; }} }}
</style>
</head>
<body onload="window.print()">
{invoice_rendered_html}
</body>
</html>"""

        with c_act1:
            st.download_button(
                label="📥 Download Invoice (HTML)",
                data=full_html_document,
                file_name=f"Invoice_{inv['invoice_id']}.html",
                mime="text/html",
                use_container_width=True
            )

        # ASCII Plain Text Receipt (100% matched to original project terminal output)
        text_receipt = io.StringIO()
        text_receipt.write("=" * 48 + "\n")
        text_receipt.write(f"           {STORE_NAME}\n")
        text_receipt.write(f"           OFFICIAL STORE BILL\n")
        text_receipt.write("=" * 48 + "\n")
        text_receipt.write(f"Invoice No : {inv['invoice_id']}\n")
        text_receipt.write(f"Date & Time: {inv['timestamp']}\n")
        text_receipt.write(f"Customer   : {inv['customer_name']}\n")
        text_receipt.write(f"Contact    : {inv['customer_phone']}\n")
        text_receipt.write(f"Payment    : {inv['payment_method']}\n")
        text_receipt.write("-" * 48 + "\n")
        text_receipt.write(f"{'Product':<16}{'Qty':>6}{'Price':>12}{'Amount':>12}\n")
        text_receipt.write("-" * 48 + "\n")
        for itm in inv["items"]:
            text_receipt.write(
                f"{itm['name'][:15]:<16}{itm['quantity']:>6}"
                f"Rs.{itm['price']:>9.2f}Rs.{itm['amount']:>9.2f}\n"
            )
        text_receipt.write("-" * 48 + "\n")
        text_receipt.write(f"{'Subtotal:':>34} Rs.{inv['subtotal']:>10.2f}\n")
        text_receipt.write(f"{'CGST (2.5%):':>34} Rs.{inv['cgst']:>10.2f}\n")
        text_receipt.write(f"{'SGST (2.5%):':>34} Rs.{inv['sgst']:>10.2f}\n")
        text_receipt.write(f"{'Tax (5%):':>34} Rs.{inv['tax']:>10.2f}\n")
        text_receipt.write(f"{'Total:':>34} Rs.{inv['grand_total']:>10.2f}\n")
        text_receipt.write("=" * 48 + "\n")
        text_receipt.write(f"Words: {inv['amount_words']}\n")
        text_receipt.write("Thank you for shopping with us!\n")

        with c_act2:
            st.download_button(
                label="📄 Download Receipt (Text)",
                data=text_receipt.getvalue(),
                file_name=f"Receipt_{inv['invoice_id']}.txt",
                mime="text/plain",
                use_container_width=True
            )

        with c_act3:
            if st.button("➕ Start Next Customer Bill", use_container_width=True):
                st.session_state.current_invoice = None
                st.session_state.customer_name = "Walk-in Customer"
                st.session_state.customer_phone = "9876543210"
                st.rerun()


# ==============================================================================
# VIEW 3: INVENTORY MANAGEMENT
# ==============================================================================
elif selected_view == "📊 Inventory Management":
    st.markdown("### 📊 Inventory Stock Control & Catalog Management")
    st.caption("Add new SKU items, restock existing inventory, modify retail pricing, or prune catalog items.")

    tab_add, tab_update, tab_delete, tab_audit = st.tabs([
        "➕ Add New Product",
        "🔄 Restock & Update Price",
        "❌ Remove Discontinued Product",
        "📋 Full Warehouse Audit"
    ])

    # TAB 1: ADD NEW PRODUCT
    with tab_add:
        st.markdown("""
        <div class="content-card">
            <div class="card-title">📦 Register New Product in Inventory</div>
        """, unsafe_allow_html=True)

        with st.form("form_add_product", clear_on_submit=True):
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                new_code = st.text_input("Product Code (Unique SKU)", placeholder="e.g. P111").strip().upper()
                new_name = st.text_input("Product Name", placeholder="e.g. Basmati Rice (1kg)").strip()
            with col_a2:
                new_price = st.number_input("Retail Unit Price (₹)", min_value=0.50, max_value=50000.0, value=50.0, step=1.0)
                new_stock = st.number_input("Initial Inflow Stock Quantity", min_value=0, max_value=50000, value=20, step=1)

            submit_add = st.form_submit_button("Register Product to Catalog", type="primary")

            if submit_add:
                if not new_code or not new_name:
                    st.error("Both Product Code and Product Name are strictly required.")
                elif new_code in st.session_state.inventory:
                    st.error(f"Product Code '{new_code}' already exists ({st.session_state.inventory[new_code]['name']}). Choose a unique code.")
                else:
                    st.session_state.inventory[new_code] = {
                        "name": new_name,
                        "price": float(new_price),
                        "stock": int(new_stock)
                    }
                    save_inventory_to_file(st.session_state.inventory)
                    st.success(f"Product '{new_name}' (Code: {new_code}) successfully registered with {new_stock} units at ₹{new_price:.2f}!")
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 2: RESTOCK / UPDATE PRICE
    with tab_update:
        st.markdown("""
        <div class="content-card">
            <div class="card-title">🔄 Restock Inward Shipment or Update Retail Price</div>
        """, unsafe_allow_html=True)

        if st.session_state.inventory:
            selected_upd_code = st.selectbox(
                "Select Existing Product",
                options=list(st.session_state.inventory.keys()),
                format_func=lambda c: f"{c} - {st.session_state.inventory[c]['name']} (Current Stock: {st.session_state.inventory[c]['stock']}, Price: ₹{st.session_state.inventory[c]['price']:.2f})"
            )

            curr_item = st.session_state.inventory[selected_upd_code]

            with st.form("form_update_product"):
                col_u1, col_u2 = st.columns(2)
                with col_u1:
                    updated_price = st.number_input(
                        "Updated Retail Price (₹)",
                        min_value=0.50,
                        max_value=50000.0,
                        value=float(curr_item["price"]),
                        step=1.0
                    )
                    stock_adjustment_type = st.radio(
                        "Stock Adjustment Mode",
                        ["Add New Shipment Quantity (+)", "Overwrite Absolute Stock Level"]
                    )
                with col_u2:
                    if stock_adjustment_type == "Add New Shipment Quantity (+)":
                        add_units = st.number_input("Inward Units to Add", min_value=0, max_value=50000, value=10, step=1)
                        target_stock = curr_item["stock"] + add_units
                        st.caption(f"New stock will become: **{target_stock} units** (Current: {curr_item['stock']} + Inward: {add_units})")
                    else:
                        target_stock = st.number_input("Set Absolute Stock Level", min_value=0, max_value=50000, value=int(curr_item["stock"]), step=1)

                submit_update = st.form_submit_button("Update Product Record", type="primary")

                if submit_update:
                    curr_item["price"] = float(updated_price)
                    curr_item["stock"] = int(target_stock)
                    save_inventory_to_file(st.session_state.inventory)
                    st.success(f"Product '{curr_item['name']}' updated: Stock = {target_stock} units, Price = ₹{updated_price:.2f}.")
                    st.rerun()
        else:
            st.info("No items in inventory to update.")

        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 3: REMOVE PRODUCT
    with tab_delete:
        st.markdown("""
        <div class="content-card">
            <div class="card-title">❌ Decommission / Delete Product</div>
        """, unsafe_allow_html=True)

        if st.session_state.inventory:
            del_code = st.selectbox(
                "Choose Product to Decommission",
                options=list(st.session_state.inventory.keys()),
                format_func=lambda c: f"{c} - {st.session_state.inventory[c]['name']} (Stock: {st.session_state.inventory[c]['stock']})"
            )

            del_item = st.session_state.inventory[del_code]
            st.warning(f"Are you sure you want to permanently remove **{del_item['name']}** ({del_code}) from the active inventory catalog?")

            col_del1, _ = st.columns([1, 3])
            with col_del1:
                if st.button("Confirm Deletion", type="primary"):
                    del st.session_state.inventory[del_code]
                    save_inventory_to_file(st.session_state.inventory)
                    st.success(f"Product {del_code} removed.")
                    st.rerun()
        else:
            st.info("Inventory is empty.")

        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 4: AUDIT TABLE
    with tab_audit:
        st.markdown("""
        <div class="content-card">
            <div class="card-title">📋 Comprehensive Inventory Audit Log</div>
        """, unsafe_allow_html=True)

        all_items = [
            {
                "Product Code": c,
                "Name": itm["name"],
                "Unit Price (₹)": itm["price"],
                "Stock (Units)": itm["stock"],
                "Stock Status": "Low Stock" if itm["stock"] <= 5 else ("Out of Stock" if itm["stock"] == 0 else "In Stock"),
                "Total Valuation (₹)": itm["price"] * itm["stock"]
            }
            for c, itm in st.session_state.inventory.items()
        ]

        df_all = pd.DataFrame(all_items)
        st.dataframe(df_all, use_container_width=True, hide_index=True)

        # CSV Download Button
        csv_buffer = io.StringIO()
        df_all.to_csv(csv_buffer, index=False)
        st.download_button(
            label="📥 Export Inventory Audit as CSV",
            data=csv_buffer.getvalue(),
            file_name=f"Warehouse_Inventory_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

        st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# VIEW 4: INVOICE ARCHIVE & REPORTS
# ==============================================================================
elif selected_view == "📑 Invoice History":
    st.markdown("### 📑 Transaction Archive & Fiscal Audit Reports")
    st.caption("Audit all receipts issued during this runtime session with instant re-printing and sales telemetry.")

    if st.session_state.invoices:
        total_revenue = sum(inv["grand_total"] for inv in st.session_state.invoices)
        total_tax_collected = sum(inv["tax"] for inv in st.session_state.invoices)
        total_items_sold = sum(sum(item["quantity"] for item in inv["items"]) for inv in st.session_state.invoices)
        avg_order_value = total_revenue / len(st.session_state.invoices)

        c_rev1, c_rev2, c_rev3, c_rev4 = st.columns(4)
        with c_rev1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Cumulative Gross Revenue</div>
                <div class="kpi-value">₹{total_revenue:,.2f}</div>
                <div class="kpi-sub">Across {len(st.session_state.invoices)} completed transactions</div>
            </div>
            """, unsafe_allow_html=True)
        with c_rev2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Tax Collected (5%)</div>
                <div class="kpi-value">₹{total_tax_collected:,.2f}</div>
                <div class="kpi-sub">CGST + SGST remittance</div>
            </div>
            """, unsafe_allow_html=True)
        with c_rev3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Units Liquidated</div>
                <div class="kpi-value">{total_items_sold}</div>
                <div class="kpi-sub">Total product units billed</div>
            </div>
            """, unsafe_allow_html=True)
        with c_rev4:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Average Order Value (AOV)</div>
                <div class="kpi-value">₹{avg_order_value:,.2f}</div>
                <div class="kpi-sub">Per invoice ticket size</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="content-card">
            <div class="card-title">📜 Past Tax Invoices</div>
        """, unsafe_allow_html=True)

        inv_summary = []
        for inv in reversed(st.session_state.invoices):
            inv_summary.append({
                "Invoice ID": inv["invoice_id"],
                "Date & Time": inv["timestamp"],
                "Customer": inv["customer_name"],
                "Contact": inv["customer_phone"],
                "Items Count": len(inv["items"]),
                "Payment": inv["payment_method"],
                "Tax (5%)": f"₹{inv['tax']:.2f}",
                "Grand Total": f"₹{inv['grand_total']:.2f}"
            })

        st.dataframe(pd.DataFrame(inv_summary), use_container_width=True, hide_index=True)

        # Select invoice to reprint
        st.markdown("---")
        st.markdown("#### 🖨️ Re-inspect or Re-print Past Invoice")
        invoice_options = [inv["invoice_id"] for inv in st.session_state.invoices]
        selected_inv_id = st.selectbox("Select Invoice ID", invoice_options)

        matching_inv = next((inv for inv in st.session_state.invoices if inv["invoice_id"] == selected_inv_id), None)
        if matching_inv:
            if st.button("Set as Active Invoice to View/Download"):
                st.session_state.current_invoice = matching_inv
                st.info(f"Loaded invoice {selected_inv_id}. Switch to 'Billing & Checkout' view to download or print it!")

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="content-card" style="text-align: center; padding: 48px 16px;">
            <div style="font-size: 40px; margin-bottom: 12px;">📑</div>
            <div style="font-size: 16px; font-weight: 600; color: #475569;">No Invoices Generated Yet</div>
            <p style="font-size: 13px; color: #94A3B8;">Completed orders and printable tax receipts will appear here automatically.</p>
        </div>
        """, unsafe_allow_html=True)


# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("""
<div style="text-align: center; margin-top: 48px; padding-top: 24px; border-top: 1px solid #E2E8F0; font-size: 12px; color: #94A3B8;">
    <b>Retail Billing and Inventory Management System</b> • Python & Streamlit Implementation<br>
    Built for academic demonstration & enterprise point-of-sale prototyping.
</div>
""", unsafe_allow_html=True)

