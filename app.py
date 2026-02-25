from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Expense
from datetime import datetime, date
from sqlalchemy import extract, func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'expense-tracker-secret-key'

db.init_app(app)

CATEGORIES = [
    'Food & Dining',
    'Transportation',
    'Shopping',
    'Entertainment',
    'Health & Fitness',
    'Bills & Utilities',
    'Travel',
    'Education',
    'Personal Care',
    'Other'
]

@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    today = date.today()
    selected_month = request.args.get('month', today.strftime('%Y-%m'))

    try:
        year, month = map(int, selected_month.split('-'))
    except ValueError:
        year, month = today.year, today.month
        selected_month = today.strftime('%Y-%m')

    expenses = Expense.query.filter(
        extract('year', Expense.date) == year,
        extract('month', Expense.date) == month
    ).order_by(Expense.date.desc(), Expense.created_at.desc()).all()

    monthly_total = db.session.query(func.sum(Expense.amount)).filter(
        extract('year', Expense.date) == year,
        extract('month', Expense.date) == month
    ).scalar() or 0.0

    category_totals = db.session.query(
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).filter(
        extract('year', Expense.date) == year,
        extract('month', Expense.date) == month
    ).group_by(Expense.category).order_by(func.sum(Expense.amount).desc()).all()

    available_months = db.session.query(
        func.strftime('%Y-%m', Expense.date).label('month')
    ).distinct().order_by(func.strftime('%Y-%m', Expense.date).desc()).all()

    available_months = [m.month for m in available_months]
    if selected_month not in available_months:
        available_months.insert(0, selected_month)

    return render_template(
        'index.html',
        expenses=expenses,
        monthly_total=monthly_total,
        category_totals=category_totals,
        categories=CATEGORIES,
        selected_month=selected_month,
        available_months=available_months,
        today=today.strftime('%Y-%m-%d')
    )

@app.route('/add', methods=['POST'])
def add_expense():
    amount = request.form.get('amount', '').strip()
    category = request.form.get('category', '').strip()
    note = request.form.get('note', '').strip()
    expense_date = request.form.get('date', '').strip()

    errors = []

    if not amount:
        errors.append('Amount is required.')
    else:
        try:
            amount = float(amount)
            if amount <= 0:
                errors.append('Amount must be a positive number.')
        except ValueError:
            errors.append('Amount must be a valid number.')

    if not category or category not in CATEGORIES:
        errors.append('Please select a valid category.')

    if not expense_date:
        errors.append('Date is required.')
    else:
        try:
            expense_date = datetime.strptime(expense_date, '%Y-%m-%d').date()
        except ValueError:
            errors.append('Invalid date format.')

    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('index'))

    expense = Expense(
        amount=amount,
        category=category,
        note=note,
        date=expense_date
    )
    db.session.add(expense)
    db.session.commit()
    flash('Expense added successfully!', 'success')

    selected_month = expense_date.strftime('%Y-%m')
    return redirect(url_for('index', month=selected_month))

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    selected_month = expense.date.strftime('%Y-%m')
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('index', month=selected_month))

@app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if request.method == 'POST':
        amount = request.form.get('amount', '').strip()
        category = request.form.get('category', '').strip()
        note = request.form.get('note', '').strip()
        expense_date = request.form.get('date', '').strip()

        errors = []

        if not amount:
            errors.append('Amount is required.')
        else:
            try:
                amount = float(amount)
                if amount <= 0:
                    errors.append('Amount must be a positive number.')
            except ValueError:
                errors.append('Amount must be a valid number.')

        if not category or category not in CATEGORIES:
            errors.append('Please select a valid category.')

        if not expense_date:
            errors.append('Date is required.')
        else:
            try:
                expense_date = datetime.strptime(expense_date, '%Y-%m-%d').date()
            except ValueError:
                errors.append('Invalid date format.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('index'))

        expense.amount = amount
        expense.category = category
        expense.note = note
        expense.date = expense_date
        db.session.commit()
        flash('Expense updated successfully!', 'success')

        selected_month = expense_date.strftime('%Y-%m')
        return redirect(url_for('index', month=selected_month))

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)