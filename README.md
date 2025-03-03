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
    /.idea
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
     > .\venv\Scripts\Activate (For Windows)
     pip install -r requirements.txt
     ```
   - Run the server:
     ```bash
     cd backend/
     python app.py
     ```

## Deployment to Existing Web Application
1. Add ```<script src="{{ url_for('static', filename='tracker.js') }}"></script>``` into your existing HTML file
2. Under tracker.js, amend ```fetch('http://x.x.x.x/api/analysis-metrics'``` to fit your server IP address
3. Ensure that recaptcha.js and tracker.js are stored in static/ to allow API calling

**Note to Prof: Hello. We'll be hosting the server specified in the code that is running this solution until next trimester for your grading if you wish you see it!**
