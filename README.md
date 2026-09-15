# ExpensePilot

ExpensePilot is a lightweight expense tracker built with Python and Flask. It helps users record expenses, organize spending by category, and view a simple spending summary.

## Features

- Add expenses with a title, amount, category, date, and notes
- View recorded expenses in reverse chronological order
- Delete expenses
- View total spending
- View transaction count
- View spending totals by category
- Store data locally in SQLite
- Responsive browser-based interface

## Technology stack

- Python 3.12+
- Flask 3.0.3
- Flask-SQLAlchemy 3.1.1
- SQLite
- Jinja2
- HTML and CSS

## Project structure

```text
Expense Tracker Project/
├── app/
│   ├── __init__.py
│   └── main.py
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   └── index.html
├── .gitignore
├── plan.md
├── README.md
├── requirements.txt
└── .venv/                 # Local virtual environment, not committed
```

## Prerequisites

Install the following tools:

- Python 3.12 or later
- Git

## Local setup

From the project directory, create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the development server:

```powershell
python -m flask --app app.main run --debug
```

Open the application at:

```text
http://127.0.0.1:5000
```

## Using the application

1. Open the local URL in a browser.
2. Enter an expense title, amount, category, date, and optional notes.
3. Select **Save Expense**.
4. Review the expense list, total spending, and category summary.
5. Use **Delete** to remove an expense.

The SQLite database is created automatically when the application starts. Local database files are excluded from Git by `.gitignore`.

## Testing the local endpoint

With the development server running, use PowerShell:

```powershell
curl.exe -I http://127.0.0.1:5000
```

A successful response returns HTTP `200 OK`.

## Deployment

The project plan targets Vercel for deployment. Before production deployment:

1. Set `DATABASE_URL` to a production database connection string in Vercel if data must persist between function invocations.
2. Set `SECRET_KEY` in the Vercel project environment variables.
3. Without `DATABASE_URL`, Vercel uses a writable `/tmp` SQLite database for basic operation; this storage is temporary and can be reset between deployments or function instances.
4. Add automated tests and a deployment configuration as the application grows.
5. Deploy with the Vercel CLI or connect the GitHub repository in the Vercel dashboard.

## Repository

GitHub: https://github.com/konduru939/ExpensePilot

## Project status

The current version is a local MVP with expense creation, listing, deletion, totals, and category summaries. Budget management, authentication, advanced reports, and production deployment are planned next.
