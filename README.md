# Daily Expense Tracker

A simple single-page web application to log daily expenses with category, amount, and note fields. It displays a running monthly total so you can keep track of your spending at a glance.

## Features

- Add expenses with a category, amount, and optional note
- View all expenses in a clean, sortable list
- See a running total for the current month
- Delete individual expense entries
- Persistent storage using SQLite via SQLAlchemy

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/daily-expense-tracker.git
   cd daily-expense-tracker
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Running the App

```bash
python app.py
```

Then open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Project Structure

```
daily-expense-tracker/
├── app.py               # Flask application and routes
├── models.py            # SQLAlchemy database models
├── requirements.txt     # Python dependencies
├── static/
│   └── style.css        # Application styles
├── templates/
│   └── index.html       # Main HTML template
└── README.md            # This file
```

## Usage

1. Fill in the **Category** (e.g., Food, Transport, Entertainment), **Amount**, and an optional **Note**.
2. Click **Add Expense** to save the entry.
3. The expense will appear in the list below with the date it was added.
4. The **Monthly Total** at the top updates automatically to reflect all expenses logged in the current month.
5. Click the **Delete** button next to any entry to remove it.

## Categories

Some suggested categories to get you started:

- Food & Dining
- Transport
- Housing
- Entertainment
- Health & Fitness
- Shopping
- Utilities
- Other

## License

This project is licensed under the MIT License. Feel free to use and modify it for your own purposes.