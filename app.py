import backend_functions
import mysql.connector
import configparser

config=configparser.ConfigParser()
config.read('config.ini')

host = config['Database']['host']
user = config['Database']['user']
password = config['Database']['password']

def run_app(host=host, user=user, password=password):
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

run_app()