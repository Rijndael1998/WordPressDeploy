#!/bin/python3
import Settings
import mysql.connector

database = mysql.connector.connect(host=Settings.Database.host, user=Settings.Database.user)
connector = database.cursor()

for website in Settings.websites:
    website.database.createDatabaseAndUser(connector)

