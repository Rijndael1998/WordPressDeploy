import json, O

with open("config.json") as f:
    config = json.loads(f.read())

class Database:
    host = config["database"]["host"]
    user = config["database"]["user"]
    password = config["database"]["password"]

websites = [ O.Website(website) for website in config["websites"] ]

    

del json