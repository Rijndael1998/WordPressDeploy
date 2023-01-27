import json, O

with open("config.json") as f:
    config = json.loads(f.read())

class Database:
    host = config["database"]["host"]
    user = config["database"]["user"]
    password = config["database"]["password"]

secrets = [website["database"]["password"] for website in config["websites"]]
secrets.append(Database.password)

websites = [ O.Website(website, secrets) for website in config["websites"] ]

del json
