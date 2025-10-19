🧩 Step 2 — Environment Setup (Windows)
✅ What We’ll Build (Overview)

Your project will have:

Frontend: HTML, CSS, JS

Backend: Flask (Python)

Database: SQLite

Deployment: Render (free cloud hosting)

Version Control: Git + GitHub

The goal: a fully working app where users can view food items, add them to a cart, and place an order — with admin management.

🛠️ Step 2.1 — Install Python

Visit https://www.python.org/downloads/

Download the latest Python 3.x for Windows.

During installation:

✅ Check “Add Python to PATH”

Click Install Now

To verify installation:

python --version

🧰 Step 2.2 — Create Project Folder

In your Documents or Desktop, create a folder:

C:\Users\<YourName>\Documents\food_ordering_system


Open VS Code → click File > Open Folder → choose this folder.

💻 Step 2.3 — Create Virtual Environment

Open the VS Code terminal (Ctrl + `) and run:

python -m venv venv


Activate it:

venv\Scripts\activate


You should now see (venv) in your terminal prompt — that’s good.

📦 Step 2.4 — Install Flask and Dependencies

Run this:

pip install flask flask_sqlalchemy flask_cors


We’re installing:

flask → backend web framework

flask_sqlalchemy → database ORM

flask_cors → for frontend-backend communication (if needed)
