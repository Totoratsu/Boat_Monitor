from mqtt.client import Client
import json, os


filePath = os.path.dirname(os.path.realpath(__file__))
logsPath = os.path.join(filePath, "..", "logs")

def deleteDir(journey: str):
    name = journey + ".json"
    path = os.path.join(logsPath, "journey", name)

    os.remove(path)

def saveJourney(journey: dict):
    name = str(journey["journey_id"]) + ".json"
    path = os.path.join(logsPath, "journey", name)

    f = open(path, "w")
    f.write(json.dumps(journey, indent=4))
    f.close()

def saveToken(token: str, journey: str):
    name = journey + ".json"
    path = os.path.join(logsPath, "token", name)

    f = open(path, "w")
    f.write("{\n\t\"token\": \"" + token + "\"\n}")
    f.close()

def getWeight():
    # I think I'll get this through some sensor reading
    return 0.0

def processMessage(msg: dict, client: Client):
    response = {}

    if "start" in msg:
        if "journey_id" in msg and msg["journey_id"] != 0:
            if msg["start"] == 1:
                response["weight"] = msg["weight"]

                saveToken(msg["token"], msg["journey_id"])
                response["token"] = msg["token"]

                client.publish("DEPARTURE", json.dumps(response, indent=4))
                
            response["started"] = 1
            saveJourney(msg["journey_id"]) 
    
    elif "end" in msg and msg["end"] == 1:
        if "journey_id" in msg and msg["journey_id"] != 0:
            response["started"] = 0
            response["weight"] = getWeight()
            response["token"] = msg["token"]
            response["journey_id"] = msg["journey_id"]

            saveJourney(response)

            client.currentJourney = 0 # end journey
            client.publish("END", json.dumps(response, indent=4))

    elif "delete" in msg and msg["delete"] == 1:
        if "journey_id" in msg and msg["journey_id"] != 0:
            if client.currentJourney != msg["journey_id"]:
                response["proceed"] = 1
                client.publish("DELETION", json.dumps(response, indent=4))

                deleteDir(str(msg["journey_id"]))

                response["deleted"] = 1
                client.publish("DELETION", json.dumps(response, indent=4))
