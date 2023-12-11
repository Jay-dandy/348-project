# Run Project:
- Note* 
  - feedback Loop:
    As you test and encounter issues, modify your application accordingly, and retest.
    If you make changes to your database structure or models, remember to update and rerun init_db.py if necessary.
# Backend: 
Implement a search endpoint that takes a query string and returns matching algorithms and data structures. This could be a single endpoint with a type filter (to differentiate between algorithms and data structures) or separate endpoints for each.

# Frontend: 
Have a search bar on the main page. When the user types in and submits a query, make an AJAX call to the backend's search endpoint. Based on the result, redirect the user to the appropriate details page.

# Connection & Configuration for Google Cloud (Notes):
- You can configure your local development environment to connect to the Google Cloud SQL instance by using its connection string. Ensure you install the necessary database drivers for your application based on the type of database you're using (PostgreSQL, MySQL, etc.).

- Google Cloud SQL does not allow connections from any IP address by default. To connect from your local machine, you'll need to whitelist your IP address in the Cloud SQL instance's settings. Remember, it's crucial to be cautious and avoid whitelisting a broad range of IPs.

# Directory Structure of Project:
- static: Contains static files like CSS and JavaScript.
- /templates: Contains the HTML templates used by Flask.
- /models: Contains the database models.
- /routes: Contains the routes/views of your Flask application.
- run.py: Entry point for running the Flask application.
- requirements.txt: Lists all the Python packages required for the project.

# To activate this environment, use
- conda activate algo_project

# To deactivate an active environment, use
- conda deactivate

# To adjust path
- export PATH=$(echo $PATH | tr ':' '\n' | grep -v ".pyenv/shims" | tr '\n' ':')

# Update requirements.txt:
- conda list --export > requirements.txt

# Google Cloud (Project info):
- Project ID: cs-348-project-403805
- cs-348-postgre Public IP: 35.243.227.185
- Password for PostgreSQL instance: fuggg1
- InstanceID: cs-348-project-postgre
- DB name: algos_ds_db
- firewall rule name: my-ip
- target tag: flask-app
- Firewall rule specified ip: 104.28.104.207/32 
- Firewal port: tcp 5432
- Username of postgres DB user: postgres
- Password of postgres DB user: this-348-pdub

# Environment Variables to allow DB connection:
export DB_USER='postgres'
export DB_PASSWORD='fuggg1'
export PUBLIC_IP='35.243.227.185'
export DB_NAME='algos_ds_db'

# Manually connecting to db:
*Note config.py handles this when the program runs*
1) Make sure the environment variables mentioned in the above
section are set.
2) psql postgresql://postgres@35.243.227.185/algos_ds_db
Then enter password: fugg1
<!-- postgresql+psycopg2://postgres:fuggg1@35.243.227.185/algos_ds_db
psql postgresql://postgres:fuggg1@35.243.227.185/algos_ds_db -->

 # path to pip
/Users/justinschoch/anaconda3/envs/algo_project/bin/pip

# Running app
1) set OS env variables for DB
2) run 'python init_db.py'
3) run 'python run.py'

# Woking with DB
- If you make a chaange to a table you need to drop the table and recreate as follows:
  1) open terminal and connect to DB:
       psql postgresql://postgres@35.243.227.185/algos_ds_db
  2) run \dt to show tables
  3) run DROP TABLE IF EXISTS "user";  //user as an example, no need for quotes most of the time
  4) rebuild project: python init_db.py and run.py
- example command to add column in psql: ALTER TABLE algorithm ADD COLUMN user_id INTEGER REFERENCES "user"(id);


# Created indexes and stored procedures:
<!-- username index for quick login lokup:
since users will be logging in with their 
username, an index on the username column of 
the user table will make this lookup faster -->
- CREATE INDEX idx_username ON "user" (username);

<!-- user ID indexes on DS and algos.:
they speed up queries to fetch DS and 
algorithms belonging to a specific user. -->
- CREATE INDEX idx_datastructure_userid ON data_structure(user_id);
- CREATE INDEX idx_algorithm_userid ON algorithm(user_id);

<!-- name index for quick lookups:
Users may also look up data structures 
and algorithms by name, so an index on 
the name column can be beneficial. -->
- CREATE INDEX idx_datastructure_name ON data_structure(name);
- CREATE INDEX idx_algorithm_name ON algorithm(name);

