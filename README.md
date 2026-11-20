# Fridge Restock App

## Requirements
- Python 3.9+
- Flask

## Run on Windows
1. Extract the ZIP folder.
2. Open PowerShell or Command Prompt inside the extracted folder.
3. Install dependencies:
   `python -m pip install -r requirements.txt`
4. Start:
   `python app.py`
5. Open in your browser:
   `http://127.0.0.1:5000`

## Features
- Manually add fridge items
- Quantity and minimum-stock tracking
- Add or take out one unit with quick buttons
- Restock list automatically updates based on minimum quantity
- Expiry date field
- Search and stock filters
- Delete items
- SQLite local database persists inventory

Note: “Taken Out” is a manual action; the app cannot physically detect food removal without connected sensors/camera.
