from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Expense
from datetime import datetime
import calendar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    month_name = calendar.month_name[current_month]

    expenses = Expense.query.filter(
        db.extract('month', Expense.date) == current_month,
        db.extract('year', Expense.date) == current_year
    ).order_by(Expense.date.desc()).all()

    monthly_total = sum(e.amount for e in expenses)

    categories = [
        'Food & Dining',
        'Transportation',
        'Housing',
        'Entertainment',
        'Health & Fitness',
        'Shopping',
        'Utilities',
        'Education',
        'Travel',
        'Other'
    ]

    category_totals = {}
    for expense in expenses:
        if expense.category not in category_totals:
            category_totals[expense.category] = 0
        category_totals[expense.category] += expense.amount

    return render_template(
        'index.html',
        expenses=expenses,
        monthly_total=monthly_total,
        month_name=month_name,
        current_year=current_year,
        categories=categories,
        category_totals=category_totals
    )


@app.route('/add', methods=['POST'])
def add_expense():
    category = request.form.get('category')
    amount = request.form.get('amount')
    note = request.form.get('note', '')

    if not category or not amount:
        return redirect(url_for('index'))

    try:
        amount = float(amount)
        if amount <= 0:
            return redirect(url_for('index'))
    except ValueError:
        return redirect(url_for('index'))

    expense = Expense(
        category=category,
        amount=amount,
        note=note,
        date=datetime.now()
    )

    db.session.add(expense)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/api/expenses')
def api_expenses():
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    expenses = Expense.query.filter(
        db.extract('month', Expense.date) == current_month,
        db.extract('year', Expense.date) == current_year
    ).order_by(Expense.date.desc()).all()

    return jsonify([e.to_dict() for e in expenses])


if __name__ == '__main__':
    app.run(debug=True)