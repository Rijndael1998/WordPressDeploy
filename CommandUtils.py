import os


def strip(cmd, secrets):
    for secret in secrets:
        cmd = cmd.replace(secret, "*" * len(secret))

    return cmd

def runCommand(cmd, secrets):
    if os.getuid() == 0:
        print("$ >", strip(cmd, secrets))
        return os.system(cmd)
    else:
        print("pretend $ >", strip(cmd, secrets))
        return None

def runSQLQuery(connector, query, secrets):
    if os.getuid() == 0 and connector is not None:
        print("sql $ >", strip(query, secrets))
        try:
            connector.execute(query)
        except Exception as e:
            print("====Error====\n{}\n\n".format(e))
        return None #connector.fetchall()
    else:
        print("pretend sql >", strip(query, secrets))
        return None
