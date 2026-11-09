# Apex Retail Pro: Modern Web-Based Retail Billing & Inventory System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg)](https://streamlit.io/)
[![Tax Compliant](https://img.shields.io/badge/GST%20Compliant-5%25%20Standard-059669.svg)]()
[![Deployment](https://img.shields.io/badge/Deployment-Streamlit%20Cloud%20Ready-1E3A8A.svg)]()

> A modern, responsive, corporate-grade Web Point of Sale (POS) and Inventory Management System built with **Streamlit** and **Python**. Transformed from a traditional terminal-based retail script into an interactive web application designed for academic evaluation, college mini-project submissions, and live demonstration.

---

## 🌟 Live Features & Highlights

### 1. Executive Corporate Design & Color Palette
- **Primary Navy Blue (`#1E3A8A`):** Applied across top hero headers, branded navigation, primary action buttons, and invoice summaries.
- **Slate Gray Card Architecture (`#E2E8F0`, `#64748B`):** Clean borders, card surfaces, and subtle elevation shadows.
- **Crisp White Canvas (`#FFFFFF`, `#F8FAFC`):** Optimal readability and high-contrast tables.
- **Subtle Emerald Highlights (`#059669`, `#10B981`):** Indicates healthy stock levels, order success notifications, and payment confirmations.
- **Clean Sans-Serif Typography:** Rendered with standard *Inter* and modern system UI fonts.

### 2. Module Breakdown
* **📦 Product Catalog:**
  - Real-time catalog table displaying Product Code, Product Name, Unit Price (₹), and Physical Stock.
  - Interactive Stock Progress meters with automatic badge indicators:
    - 🟢 **Available (>5 units):** Normal healthy stock level.
    - 🟡 **Low Stock (≤5 units):** Immediate visual alert for replenishment.
    - 🔴 **Out of Stock (0 units):** Automatically locks ordering.
  - Multi-parameter search (filter by SKU code or product name) and stock health filters.
  - One-click *Quick Add* directly from catalog.

* **🧾 Interactive Billing & Checkout:**
  - Customer information input (Customer Name, Mobile Number, Payment Method: UPI, Cash, Card, Net Banking).
  - Dynamic quantity selector with **real-time ceiling validation** (prevents selecting more than current warehouse stock or already-reserved cart units).
  - Live financial computation:
    - **Subtotal:** Sum of line item amounts.
    - **CGST (2.5%):** Central Goods & Services Tax.
    - **SGST (2.5%):** State Goods & Services Tax.
    - **Total Tax (5%):** Preserves original project tax model (`TAX_RATE = 0.05`).
    - **Grand Total (₹):** Auto-calculated and converted into formal Indian Rupee words (e.g., *"One Hundred Fifty-Seven Rupees and Fifty Paise Only"*).

* **🖨️ Real Retail Tax Invoice Generation:**
  - Styled after authentic retail tax invoices (Store GSTIN, CIN, serial invoice numbers, cashier ID, itemized rate & tax breakdown).
  - **Download as Printable HTML:** Comes pre-loaded with `@media print` CSS so clicking print or `Ctrl+P` opens a clean thermal/A4 invoice without web UI elements.
  - **Download as ASCII Text Receipt:** Retains exact compatibility with the original console receipt format.

* **📊 Warehouse Inventory Control:**
  - **Add New Product:** Create unique SKU codes, descriptions, unit rates, and initial stock quantities.
  - **Restock & Adjust:** Support for inward supplier shipments (`+` units) or direct stock overwrite.
  - **Decommission Item:** Safe product removal with confirmation safeguard.
  - **CSV Audit Export:** Download full warehouse ledger in one click.

* **📑 Invoice Archive & Telemetry:**
  - Audit log of all completed transactions during the session.
  - Live revenue telemetry: Cumulative Gross Revenue, Total Tax Remitted, Units Sold, and Average Order Value (AOV).
  - One-click historical invoice reload and reprint.

---

## 📂 Project Structure

```text
Pminiproject/
│
├── app.py                      # Complete Streamlit Web Application
├── inventory.txt               # Persistent text database (code,name,price,stock)
├── requirements.txt            # Lightweight production dependencies
├── README.md                   # Complete documentation & college report guide
└── .streamlit/
    └── config.toml             # Corporate theme configuration (Navy & Slate)
```

---

## 🚀 How to Run Locally

### Prerequisites
Make sure Python 3.9 or higher is installed on your machine.

### 1. Clone or Open Workspace
Open a terminal in the project directory:
```bash
cd "c:\Users\lenovo\Desktop\Pminiproject"
```

### 2. Create and Activate Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
Your default browser will automatically open to `http://localhost:8501`.

---

## 🌐 Instant Public URL Deployment (For College Submission)

To generate a live public URL (e.g. `https://apex-retail-pos.streamlit.app`) to share with professors and examiners:

### Method A: Streamlit Community Cloud (Recommended — Free & Instant)
1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Retail Billing & Inventory System"
   # Create a repository on github.com (e.g., retail-billing-pos)
   git remote add origin https://github.com/<your-username>/retail-billing-pos.git
   git branch -M main
   git push -u origin main
   ```
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
3. Click **"New app"**.
4. Select your repository: `<your-username>/retail-billing-pos`.
5. Set Main file path to: `app.py`.
6. Click **"Deploy!"**.
7. In ~1 minute, Streamlit gives you a **permanent live public URL** that you can submit in your college portal or presentation slides!

### Method B: Render
1. Create a free account on **[render.com](https://render.com)**.
2. Click **New +** -> **Web Service**.
3. Connect your GitHub repository.
4. Set the Build Command:
   ```bash
   pip install -r requirements.txt
   ```
5. Set the Start Command:
   ```bash
   streamlit run app.py --server.port $PORT --server.address 0.0.0.0
   ```
6. Click **Deploy Web Service**.

---

## 📋 Data Persistence Specification

The application honors the original project's file format:
- File name: `inventory.txt`
- Format: Plain text, comma-separated values (`code,name,price,stock`).
- Example:
  ```text
  P101,Rice (1kg),60.00,20
  P102,Milk (1L),30.00,15
  P103,Bread (Brown),25.00,12
  ```
Any transaction that finalizes checkout immediately updates the stock in `inventory.txt` on disk and reflects instantly across all views in the app session.

---

## 🎓 Academic Mini-Project Documentation Notes

| Field | Detail |
| :--- | :--- |
| **Project Title** | Web-Based Retail Point of Sale (POS) and Inventory Management System |
| **Language** | Python 3.x |
| **Frontend Framework** | Streamlit Component Engine with Custom Responsive CSS & Print Queries |
| **Data Architecture** | Dual-tier: In-Memory Session State Cache + Persistent Disk Flat File (`inventory.txt`) |
| **Taxation Specification** | Dual GST Scheme: Central GST (2.5%) + State GST (2.5%) = 5.0% Aggregate Rate |
| **Target Evaluation** | Real-time input validation, Stock limit constraints, Clean invoice printing, Multi-page state flow |

---

Developed for high academic performance, reliability, and enterprise presentation.

