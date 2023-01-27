""" Objects

"""
import CommandUtils


class Paths:
    def __init__(self, name):
        self.name = name
        self.paths = ["/var/www/html"]
        self.configPaths = ["/usr/local/etc/php/conf.d"]

    def generatePaths(self):
        vVars = ""
        for path in self.paths:
            safe_path = path.split("/")[-1]
            vVars += " -v " + self.name + "_vol_" + safe_path + "_" + ":" + path

        for path in self.configPaths:
            safe_path = path.split("/")[-1]
            vVars += " -v " + "configurationvol_" + safe_path + ":" + path

        return vVars


"""
This is terrible for security, but it will do for now. 
"""
class Database:
    def __init__(self, user, password, db_name):
        self.user = user
        self.password = password
        self.db_name = db_name

    def createUser(self, connector, user, domain, password, database):
        CommandUtils.runSQLQuery(connector, "create user '{}'@'{}' identified by '{}';".format(user, domain, password))
        CommandUtils.runSQLQuery(connector, "grant all privileges on {}.* to '{}'@'{}';".format(database, user, domain))

    def createDatabaseAndUser(self, connector):
        CommandUtils.runSQLQuery(connector, "create database if not exists {};".format(self.db_name))
        self.createUser(connector, self.user, "localhost", self.password, self.db_name)
        self.createUser(connector, self.user, "%", self.password, self.db_name)


def genFlag(word, value):
    return "-e {}='{}' ".format(word, value)


def genEFlags(user, password, db_name, host="192.168.0.2", table_pref="wp_"):
    eFlags = genFlag("WORDPRESS_DB_HOST", host)
    eFlags += genFlag("WORDPRESS_DB_USER", user)
    eFlags += genFlag("WORDPRESS_DB_PASSWORD", password)
    eFlags += genFlag("WORDPRESS_DB_NAME", db_name)
    eFlags += genFlag("WORDPRESS_TABLE_PREF", table_pref)
    return eFlags


class Website:
    def __init__(self, website):
        self.paths = Paths(website["database"]["database_name"])
        self.port = website["port"]
        
        self.eFlags = genEFlags(
            website["database"]["user"],
            website["database"]["password"],
            website["database"]["database_name"],
        )

        self.database = Database(
            website["database"]["user"], 
            website["database"]["password"], 
            website["database"]["database_name"]
        )

    def startDocker(self):
        vVars = "-d -p {}:80".format(self.port)
        vVars += self.paths.generatePaths() + " " + self.eFlags
        cmd = "docker run " + vVars + "wordpress"
        return CommandUtils.runCommand(cmd)
