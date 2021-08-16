## Your instructions to setup & execute the assignment.

## Parse all data from a CSV file
Python Script to collect and parse data from a csv file that as random data and store it in a SQLite database
Collect the columns and headers in different positions store them in different lists. These are saved to a database via SQLite3.


## To Run Localmachine:
Download / Clone Repo
Put the scripts in this repo into desired Directory.

# Install Python3
If you don't have Python3 installed, make sure it's on your computer. 

# Start Virtual Environment
If you don't have one yet, first enter this:

    $ virtualenv myenv

    To start the environment:
    $ env/Scripts/activate
    (env)...$

    Requirements Installation
    pip install -r requirements.txt

# Run 1-Module
(env)...$ python src/importcsv2sql.py
First we will run the script to read the csv file and store all data in sqlite 
If there is no table yet created, the program is prompted to create one. Note: all tables will be erase everytime this script is executed.

# Run Flask 
(env)...$ python app.py
if doesnt have errores you should have this 
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 144-260-320
 * Running on all addresses.
   WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://192.168.1.88:5000/ (Press CTRL+C to quit)

# Execute on Browser
Copy and Paste http://192.168.1.88:5000/ on your browser you should get home
then add http://192.168.1.88:5000//graphql, to test the GraphQL

## Run docker composer
First install docker https://docs.docker.com/engine/install/

# Execute composer
then execute this command (env)...$ docker-compose up
It takes a few minutes to create the image and install all requirements


# Todo_
Unittests
Is missing but is important to add

create better UI
create POST
