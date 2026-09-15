import os
from datetime import date
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static",
)
database_url = os.environ.get("DATABASE_URL")
if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    database_path = Path("/tmp/expensepilot.db" if os.environ.get("VERCEL") else "instance/expenses.db")
    database_path.parent.mkdir(parents=True, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path.resolve()}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "expensepilot-local-secret")

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.String(255), default="")


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    expenses = Expense.query.order_by(Expense.date.desc(), Expense.id.desc()).all()
    total_spent = sum(expense.amount for expense in expenses)
    categories = {}
    for expense in expenses:
        categories[expense.category] = categories.get(expense.category, 0) + expense.amount

    return render_template(
        "index.html",
        expenses=expenses,
        total_spent=total_spent,
        categories=sorted(categories.items()),
    )


@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    amount = request.form.get("amount", "0").strip()
    category = request.form.get("category", "General").strip() or "General"
    note = request.form.get("notes", "").strip()
    expense_date = request.form.get("date") or str(date.today())

    if not title or not amount:
        return redirect(url_for("index"))

    try:
        amount_value = float(amount)
    except ValueError:
        return redirect(url_for("index"))

    expense = Expense(
        title=title,
        amount=amount_value,
        category=category,
        date=date.fromisoformat(expense_date),
        notes=note,
    )
    db.session.add(expense)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
