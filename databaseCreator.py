import mysql.connector
from mysql.connector import connect

# Connect to MySQL
conn = connect(
    host="localhost",
    user="root",
    password="password"     # YOUR PASSWORD HERE
)

cursor = conn.cursor()

# Create DB
cursor.execute("CREATE DATABASE IF NOT EXISTS RecipeDB;")
cursor.execute("USE RecipeDB;")

# Run SQL script from table_def.sql
with open("table_def.sql", "r") as f:
    sql_commands = f.read().split(';')
    for command in sql_commands:
        if command.strip():
            cursor.execute(command)

# Run SQL script from data_insertion.sql
with open("data_insertion.sql", "r") as f:
    sql_commands = f.read().split(';')
    for command in sql_commands:
        if command.strip():
            cursor.execute(command)

conn.commit()
cursor.close()
conn.close()