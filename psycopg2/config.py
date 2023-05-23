# The name of PostgreSQL database. NOTE: The program does not create a DB. It has to be created manually through 'createdb' command or otherwise. 
DATABASE = 'clients'

# PostgreSQL user name
USERNAME = 'postgres'                 

# Directory is created upon the first launch to store password
PASSWORD_PATH = 'data/password.cfg'

# Script is ran upon the first launch to create tables and set constraints
CREATE_TABLES = 'CREATE.sql'

# The file is created upon the first launch and stores report on CREATE_TABLES script execution. Serves as an indicator that the script has already been executed at privious launches.   
FLAG = 'data/report.json'
