
from flask import Flask, render_template, url_for, abort
import json, os
from typing import Dict, Any, List

app = Flask(__name__)

def load_data() -> Dict[str, Any]:
    here = os.path.dirname(__file__)
    with open(os.path.join(here, "data.json"), "r", encoding="utf-8") as f:
        return json.load(f)

@app.context_processor
def categories_processor():
    data = load_data()
    return dict(categories=data.get("categories", []))

@app.route("/")
def index():
    data = load_data()
    products = data.get("products", [])
    return render_template("index.html", products=products)

@app.route("/category/<int:cat_id>")
def category(cat_id: int):
    data = load_data()
    cat = next((c for c in data.get("categories", []) if c["id"]==cat_id), None)
    if not cat:
        abort(404)
    products = [p for p in data.get("products", []) if p["category_id"]==cat_id]
    return render_template("category.html", category=cat, products=products)

@app.route("/product/<int:prod_id>")
def product(prod_id: int):
    data = load_data()
    prod = next((p for p in data.get("products", []) if p["id"]==prod_id), None)
    if not prod:
        abort(404)
    return render_template("product.html", product=prod)

@app.route("/top")
def top():
    data = load_data()
    # compute top by simple sales from orders (if orders exist)
    sales = {}
    for order in data.get("orders", []):
        if order.get("status") != "paid":
            continue
        for item in order.get("items", []):
            pid = item["product_id"]
            sales[pid] = sales.get(pid, 0) + item["price"]*item["quantity"]
    top_ids = sorted(sales, key=lambda x: sales[x], reverse=True)[:8]
    top_products = [p for p in data.get("products", []) if p["id"] in top_ids]
    return render_template("top.html", products=top_products)

if __name__ == "__main__":
    app.run(debug=True)
