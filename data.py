import json
import random

# game data

currentlocation = "car"
prevLocation = ""
inventory = ["fist"]

# random code
basementCode = str(random.randint(1000, 9999))
basementUnlocked = False

# flags
rangBell = False
backseatsChecked = False
gloveBoxOpen = False
ladderBroken = False
triedFrontDoor = False
birdhouseDown = False
kitchenUnlocked = False
escapeCounter = 0
insideHouse = False
basementLightOn = False
firstTimeGarden = True



# partial match
def match_item(typed, roomItems):
    typed = typed.lower().strip()
    for item in roomItems:
        if typed in item or item in typed:
            return item
    # special cases
    if "box" in typed:
        if "glove box" in roomItems or "empty glove box" in roomItems:
            if "glove box" in roomItems:
                return "glove box"
            else:
                return "empty glove box"
    if "paper" in typed:
        return "code paper"
    if "file" in typed:
        return "files"
    return typed

# rooms
rooms = {
    "car": {
        "description": "You are sitting in your parked car. The house is right outside. On the seat next to you there are old files about the case. Your backseats are a mess. There is a glove box in front of you.",
        "connections": ["garden"],
        "items": ["files", "backseats", "glove box"]
    },
    "garden": {
        "description": "You are in the front garden of the house. The house is completely dark, no lights on. But you notice a dim glow coming from an upstairs window. Probably a night lamp in the bedroom. You see an old black truck parked nearby. The fence gate is broken. You notice the front door, a ladder, a basement door, and a path to the back garden.",
        "connections": ["front door", "ladder", "basement door", "truck", "car", "back garden"],
        "items": ["stick"]
    },
    "ladder": {
        "description": "You stand next to the ladder. Its an old wooden ladder leaning against the wall. The wood looks rotten and some steps are cracked. It leads up to a window on the second floor.",
        "connections": ["garden"],
        "items": ["ladder"]
    },
    "front door": {
        "description": "You are at the front door. There is a doorbell on the wall and a small mat on the floor.",
        "connections": ["garden"],
        "items": ["door", "mat", "bell"]
    },
    "basement door": {
        "description": "You are at the basement door. There is a digital lock on it. It seems to need a code.",
        "connections": ["garden", "basement"],
        "items": ["lock"]
    },
    "basement": {
        "description": "You step into the basement. It is pitch black. You can barely make out a staircase going up. Its hard to see anything else.",
        "connections": ["basement door", "hallway"],
        "items": ["bat"]
    },
    "back garden": {
        "description": "You are in the back garden. There is a big tree with a birdhouse hanging from a branch. A door leads to the kitchen.",
        "connections": ["garden", "kitchen door"],
        "items": ["birdhouse"]
    },
    "kitchen door": {
        "description": "You are at the back door of the house. It leads to the kitchen. The door is locked.",
        "connections": ["back garden", "kitchen"],
        "items": ["door"]
    },
    "kitchen": {
        "description": "You step into the kitchen. Its dark but the moonlight helps you see. The place looks clean. Someone lives here. A hallway leads deeper into the house.",
        "connections": ["kitchen door", "hallway"],
        "items": []
    },
    "hallway": {
        "description": "You are in the hallway. It is dark and quiet. Stairs go down to the basement and up to the second floor. You see a door to what looks like a living room.",
        "connections": ["kitchen", "basement", "salon", "upstairs"],
        "items": []
    },
    "salon": {
        "description": "You enter the living room. Old furniture covered in dust. A fireplace that hasnt been used in years. A golf club leans against the wall near the door.",
        "connections": ["hallway"],
        "items": ["golf club"]
    },
    "upstairs": {
        "description": "You climb the stairs slowly. The wood creaks under your feet. The upstairs corridor is dark. Only a faint light comes from under a door at the end. The bedroom.",
        "connections": ["hallway", "bedroom"],
        "items": []
    },
    "bedroom": {
        "description": "You slowly open the bedroom door. The room is lit by a small night lamp. You see a woman tied to the bed. And next to her stands a man with a knife. The killer.",
        "connections": ["upstairs"],
        "items": []
    }
}

# save
def save_data():
    fullData = {
        "location": currentlocation,
        "prevLocation": prevLocation,
        "inventory": inventory,
        "basementCode": basementCode,
        "basementUnlocked": basementUnlocked,
        "rangBell": rangBell,
        "backseatsChecked": backseatsChecked,
        "gloveBoxOpen": gloveBoxOpen,
        "ladderBroken": ladderBroken,
        "triedFrontDoor": triedFrontDoor,
        "birdhouseDown": birdhouseDown,
        "kitchenUnlocked": kitchenUnlocked,
        "escapeCounter": escapeCounter,
        "insideHouse": insideHouse,
        "basementLightOn": basementLightOn,
        "firstTimeGarden": firstTimeGarden,
        "rooms": rooms
    }

    dataString = json.dumps(fullData, indent=4)

    f = open("savefile.json", "w")
    f.write(dataString)
    f.close()

# load
def load_data():
    global currentlocation
    global prevLocation
    global inventory
    global basementCode
    global basementUnlocked
    global rangBell
    global backseatsChecked
    global gloveBoxOpen
    global ladderBroken
    global triedFrontDoor
    global birdhouseDown
    global kitchenUnlocked
    global escapeCounter
    global insideHouse
    global basementLightOn
    global firstTimeGarden
    global rooms

    try:
        f = open("savefile.json", "r")
    except:
        print("No save file found!")
        return False
    
    fullData = json.load(f)
    
    currentlocation = fullData["location"]
    prevLocation = fullData.get("prevLocation", "")
    inventory = fullData["inventory"]
    basementCode = fullData["basementCode"]
    basementUnlocked = fullData["basementUnlocked"]
    rangBell = fullData["rangBell"]
    backseatsChecked = fullData.get("backseatsChecked", False)
    gloveBoxOpen = fullData.get("gloveBoxOpen", False)
    ladderBroken = fullData["ladderBroken"]
    triedFrontDoor = fullData.get("triedFrontDoor", False)
    birdhouseDown = fullData.get("birdhouseDown", False)
    kitchenUnlocked = fullData.get("kitchenUnlocked", False)
    escapeCounter = fullData.get("escapeCounter", 0)
    insideHouse = fullData.get("insideHouse", False)
    basementLightOn = fullData.get("basementLightOn", False)
    firstTimeGarden = fullData.get("firstTimeGarden", True)
    rooms = fullData["rooms"]

    f.close()
    return True

# item check
def check_if_item(word):
    loc = currentlocation
    roomItems = rooms[loc]["items"]
    allItems = roomItems + inventory
    allItems = allItems + ["files", "gun", "box", "glove box", "mat", "bell", "lock", "ladder", "door", "paper", "stick", "birdhouse", "key", "bat", "golf club"]
    
    for item in allItems:
        if word in item or item in word:
            return item
    return None

# place check
def check_if_place(word):
    loc = currentlocation
    connections = rooms[loc]["connections"]
    allPlaces = connections + ["garden", "car", "front door", "basement door", "basement", "truck", "back garden", "kitchen door", "tree", "kitchen", "hallway", "bedroom", "salon", "upstairs"]
    
    # living room alias
    if "living" in word or "room" in word:
        return "salon"
    
    for place in allPlaces:
        if word in place or place in word:
            return place
    return None
