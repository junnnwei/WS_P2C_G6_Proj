# User Behaviour Analysis with Adaptive Captcha

## `.gitignore` Matters
- Ensure that the .gitignore contains the following:
  ```
    # Ignore Python virtual environment
    venv/

    # Ignore Python cache files
    __pycache__/
    
    # Ignore system files
    .DS_Store
    Thumbs.db
  ```

## Frontend
- Located in the `static/` & `templates/` folder.
- `static/` contains JS file.
- `templates/` contains HTML files.

## Backend
- Located in the `backend/` folder.

## How to Run
1. **Root Directory**:
   - Set up a virtual environment and install dependencies:
     ```bash
     python -m venv venv
     > source venv/bin/activate (For MAC OS)
     > venv /bin/activate (For Windows)
     pip install -r requirements.txt
     ```
   - Run the server:
     ```bash
     cd backend/
     python app.py
     ```