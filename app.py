from backend_functions import RecipeDBConnection
import configparser

config=configparser.ConfigParser()
config.read('config.ini')

host = config['Database']['host']
user = config['Database']['user']
password = config['Database']['password']
dbname = config['Database']['dbname']


# Please use the with ... as block
# It ensures that connection commits everything to the database when the program finishes
def run_app(host=host, user=user, password=password):
    with RecipeDBConnection(host, user, password, dbname) as connection:
        print("Hi I'm a placeholder")

run_app()