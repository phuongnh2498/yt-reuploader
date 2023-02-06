import json
import os

# Data to be written


def readJSON(filename):
    isExist = os.path.exists("jsondata/{}.json".format(filename))
    if not isExist:
        with open("jsondata/{}.json".format(filename), "w") as outfile:
            json.dump({}, outfile)
        return {}
    with open("jsondata/{}.json".format(filename), "r") as openfile:
        json_object = json.load(openfile)
    return json_object


def writeJSON(data, filename):
    with open("jsondata/{}.json".format(filename), "w") as outfile:
        json.dump(data, outfile)
