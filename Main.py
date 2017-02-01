import json
import re

DefaultPath = "Test\\sharedconfig.vdf.txt" # TODO Change default path to the eqvivalent of C:\Program Files (x86)\Steam\userdata\<ID>\7\remote
WRITE_JSON_FILE = False;





def main(path=DefaultPath):
    with open(path) as file:
        string = file.read()
        string = valve2json(string)
        if (WRITE_JSON_FILE):
            out = open(path + ".json", 'w')
            out.write(string)

        parsed = json.loads(string)
        apps = parsed["UserRoamingConfigStore"]["Software"]["Valve"]["Steam"]["apps"]
        apps = {appID: apps[appID] for appID in apps if ("tags" in apps[appID]) and isinstance(apps[appID]["tags"], dict)} # remove all the games without categories

        tags = set([tagList for (appID, app) in apps.items() for (_, tagList) in app["tags"].items()])
        print(tags)




def valve2json(string):
    string = "{\n" + string + "}"
    # "txt" -> "txt":
    string = re.sub(r"(\n[^\n\"]*\"[^\n\"]*\")\n", r"\1:\n", string)
    # "txt" "bob" -> "txt": "bob",
    string = re.sub(r"([^\"\n]*\"[^\"\n]*\")([^\"\n]*)([^\"\n]*\"[^\"\n]*\")", r"\1:\2\3,", string)
    # "}" -> "},"
    string = string.replace("}","},")
    # "},}" -> "}}"
    string = re.sub(r",([\t|\n]*)\}", r"\1}", string)[0:-1]

    return string




main()




