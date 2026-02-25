# Expense Tracker

A lightweight web application for tracking daily expenses with category, amount, and notes. View running monthly totals and manage your spending with ease.

## Features

- Log expenses with category, amount, date, and optional note
- View all expenses in a clean, organized table
- See running monthly totals automatically calculated
- Delete individual expense entries
- Persistent storage using SQLite database
- Responsive, modern UI

## Requirements

- Python 3.7+
- Flask
- Flask-SQLAlchemy

## Installation

1. **Clone or download the project files**

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

```bash
python app.py
```

Then open your browser and navigate to: **http://localhost:5000**

## Usage

### Adding an Expense
1. Fill in the **Category** field (e.g., Food, Transport, Entertainment)
2. Enter the **Amount** in dollars
3. Select the **Date** of the expense
4. Optionally add a **Note** for more detail
5. Click **Add Expense**

### Viewing Monthly Totals
- The **Monthly Summary** section at the top of the page shows the total spending for the current month
- All expenses are listed in the table below, sorted by date

### Deleting an Expense
- Click the **Delete** button next to any expense entry to remove it

## Project Structure

```
expense-tracker/
├── app.py              # Main Flask application and routes
├── models.py           # SQLAlchemy database models
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── templates/
│   └── index.html      # Main HTML template
└── static/
    └── style.css       # Application styles
```

## Database

The app uses **SQLite** for data storage. The database file (`expenses.db`) is automatically created in the project root directory when the app is first run. No additional database setup is required.

## Categories

You can enter any category name you like. Common examples:
- Food & Dining
- Transportation
- Entertainment
- Shopping
- Utilities
- Healthcare
- Housing
- Personal Care

## Notes

- All amounts are stored and displayed in USD
- Dates default to today when adding a new expense
- The monthly total updates automatically as you add or delete expenses