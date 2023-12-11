# Backend: 
Implement a search endpoint that takes a query string and returns matching algorithms and data structures. This could be a single endpoint with a type filter (to differentiate between algorithms and data structures) or separate endpoints for each.

# Frontend: 
Have a search bar on the main page. When the user types in and submits a query, make an AJAX call to the backend's search endpoint. Based on the result, redirect the user to the appropriate details page.

# Connection & Configuration for Google Cloud (Notes):
- You can configure your local development environment to connect to the Google Cloud SQL instance by using its connection string. Ensure you install the necessary database drivers for your application based on the type of database you're using (PostgreSQL, MySQL, etc.).

- Google Cloud SQL does not allow connections from any IP address by default. To connect from your local machine, you'll need to whitelist your IP address in the Cloud SQL instance's settings. It's crucial to be cautious and avoid whitelisting a broad range of IPs.

# Directory Structure of Project:
- static: Contains static files like CSS and JavaScript.
- /templates: Contains the HTML templates used by Flask.
- /models: Contains the database models.
- /routes: Contains the routes/views of your Flask application.
- run.py: Entry point for running the Flask application.
- requirements.txt: Lists all the Python packages required for the project.

# Running app
1) set OS env variables for DB
2) run 'python init_db.py'
3) run 'python run.py'
