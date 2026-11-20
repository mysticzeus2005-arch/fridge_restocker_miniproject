from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("fridge.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'Other',
                quantity REAL NOT NULL DEFAULT 1,
                unit TEXT NOT NULL DEFAULT 'pcs',
                min_quantity REAL NOT NULL DEFAULT 1,
                expiry_date TEXT DEFAULT ''
            )
        """)

@app.route("/")
def home():
    with get_db() as db:
        items = db.execute("SELECT * FROM items ORDER BY name COLLATE NOCASE").fetchall()
    return render_template("index.html", items=items)

@app.route("/add", methods=["POST"])
def add_item():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "Other").strip() or "Other"
    unit = request.form.get("unit", "pcs").strip() or "pcs"
    expiry = request.form.get("expiry_date", "")
    try:
        qty = max(0, float(request.form.get("quantity", 1)))
        minimum = max(0, float(request.form.get("min_quantity", 1)))
    except ValueError:
        return redirect(url_for("home"))
    if name:
        with get_db() as db:
            db.execute(
                "INSERT INTO items (name, category, quantity, unit, min_quantity, expiry_date) VALUES (?, ?, ?, ?, ?, ?)",
                (name, category, qty, unit, minimum, expiry)
            )
    return redirect(url_for("home"))

@app.route("/item/<int:item_id>/change", methods=["POST"])
def change_quantity(item_id):
    action = request.form.get("action")
    with get_db() as db:
        item = db.execute("SELECT quantity FROM items WHERE id=?", (item_id,)).fetchone()
        if item:
            if action == "take":
                new_qty = max(0, float(item["quantity"]) - 1)
            elif action == "add":
                new_qty = float(item["quantity"]) + 1
            else:
                return redirect(url_for("home"))
            db.execute("UPDATE items SET quantity=? WHERE id=?", (new_qty, item_id))
    return redirect(url_for("home"))

@app.route("/item/<int:item_id>/delete", methods=["POST"])
def delete_item(item_id):
    with get_db() as db:
        db.execute("DELETE FROM items WHERE id=?", (item_id,))
    return redirect(url_for("home"))

@app.route("/api/items")
def api_items():
    with get_db() as db:
        items = [dict(row) for row in db.execute("SELECT * FROM items ORDER BY name").fetchall()]
    return jsonify(items)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
