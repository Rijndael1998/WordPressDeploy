#!/bin/python3
import O
import json
import mysql.connector

# Start Docker if not started
O.CommandUtils.runCommand("systemctl start docker")
O.CommandUtils.runCommand("snap start docker")

# Connect to MySQL
try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="wordpress_deploy",
    )
    connector = mydb.cursor()
except (mysql.connector.errors.DatabaseError, mysql.connector.errors.InterfaceError):
    print("Connection to sql failed. Pretending SQL...")
    connector = None

with open("websites.json") as f:
    websites = json.loads(f.read())

for website in websites:
    print("currently deploying", website["database"]["database_name"])
    Website = O.Website(website)
    Website.database.createDatabaseAndUser(connector)
    O.CommandUtils.runSQLQuery(connector, "flush privileges;")
    docker = Website.startDocker()
    print("Docker value started:", docker)
