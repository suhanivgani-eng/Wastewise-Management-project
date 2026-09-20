from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

# Demo data. Replace this list with SQLite/MySQL later.
records = [
    {"item": "Plastic Bottle", "category": "Recyclable", "quantity": 2.5, "unit": "kg", "date": "2026-09-18"},
    {"item": "Banana Peel", "category": "Organic", "quantity": 1.0, "unit": "kg", "date": "2026-09-17"},
    {"item": "Battery", "category": "Hazardous", "quantity": 0.2, "unit": "kg", "date": "2026-09-16"},
    {"item": "Laptop", "category": "E-waste", "quantity": 1, "unit": "pieces", "date": "2026-09-15"},
    {"item": "Paper Box", "category": "Recyclable", "quantity": 3.0, "unit": "kg", "date": "2026-09-14"},
]


def dashboard_stats():
    category_totals = {"Organic": 0, "Recyclable": 0, "Hazardous": 0, "E-waste": 0, "General": 0}
    for record in records:
        category = record["category"]
        category_totals[category] = category_totals.get(category, 0) + float(record["quantity"])

    total_waste = sum(float(r["quantity"]) for r in records)
    recyclable = category_totals.get("Recyclable", 0)
    organic = category_totals.get("Organic", 0)
    return {
        "total_waste": round(total_waste, 1),
        "recyclable": round(recyclable, 1),
        "organic": round(organic, 1),
        "record_count": len(records),
        "category_totals": category_totals,
    }


@app.route("/")
def dashboard():
    stats = dashboard_stats()
    return render_template("dashboard.html", stats=stats, records=records[-5:][::-1])


@app.route("/add", methods=["GET", "POST"])
def add_waste():
    if request.method == "POST":
        item = request.form.get("item", "").strip()
        category = request.form.get("category", "").strip()
        quantity = request.form.get("quantity", "").strip()
        unit = request.form.get("unit", "kg").strip()

        if not item or not category or not quantity:
            flash("Please complete all required fields.", "error")
            return redirect(url_for("add_waste"))

        try:
            quantity_value = float(quantity)
            if quantity_value <= 0:
                raise ValueError
        except ValueError:
            flash("Quantity must be a positive number.", "error")
            return redirect(url_for("add_waste"))

        records.append({
            "item": item,
            "category": category,
            "quantity": quantity_value,
            "unit": unit,
            "date": datetime.now().strftime("%Y-%m-%d"),
        })
        flash("Waste record saved successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("add.html")


@app.route("/analytics")
def analytics():
    stats = dashboard_stats()
    return render_template("analytics.html", stats=stats)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
