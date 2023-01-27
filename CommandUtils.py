import os

def runCommand(cmd):
    if os.getuid() == 0:
        print("$ >", cmd)
        return os.system(cmd)
    else:
        print("pretend $ >", cmd)
        return None

def runSQLQuery(connector, query):
    if os.getuid() == 0 and connector is not None:
        print("sql $ >", query)
        try:
            connector.execute(query)
        except Exception as e:
            print("====Error====\n{}\n\n".format(e))
        return None #connector.fetchall()
    else:
        print("pretend sql >", query)
        return None
