import data as d
from print_text import *
import sys

# commands

def handle_look():
    loc = d.currentlocation
    desc = d.rooms[loc]["description"]
    
    # basement door
    if loc == "basement door" and d.basementUnlocked:
        desc = "You are at the basement door. The lock is open. You can go inside."
    
    # garden
    if loc == "garden":
        hasStick = "stick" not in d.rooms["garden"]["items"]
        base = "You are in the front garden. The house is completely dark. But you notice a dim glow from an upstairs window. A night lamp in the bedroom."
        
        if d.ladderBroken and d.triedFrontDoor:
            desc = base + " You see a locked door, broken ladder pieces, a basement door, and the back garden."
        elif d.ladderBroken:
            desc = base + " You see the front door, broken ladder pieces, a basement door, and the back garden."
        elif d.triedFrontDoor:
            desc = base + " You see a locked door, a ladder, a basement door, and the back garden."
        else:
            desc = base + " You see the front door, a ladder, a basement door, and the back garden."
        
        if not hasStick:
            desc = desc + " There is a stick on the ground."
    
    # basement light
    if loc == "basement":
        if d.basementLightOn:
            desc = "The basement is lit by your flashlight. You see old furniture and boxes. A baseball bat leans against the wall. Stairs lead up."
        else:
            desc = "You are in the basement. It is pitch black. You can barely make out the stairs going up. Its hard to move around."
    
    print_desc(desc)


def handle_go(place):
    loc = d.currentlocation
    
    # stairs
    if loc == "basement":
        if "stair" in place or "up" in place:
            place = "hallway"
    
    # living room = salon
    if "living" in place:
        place = "salon"
    
    # match place
    matchedPlace = None
    for conn in d.rooms[loc]["connections"]:
        if place in conn or conn in place:
            matchedPlace = conn
            break
    
    if matchedPlace == None:
        print_error("You cant go there from here.")
        return False
    
    # garden intro
    if matchedPlace == "garden" and d.firstTimeGarden:
        d.firstTimeGarden = False
        print_desc("You step out of your car.")
        print_desc("The fence gate is broken. Someone forced their way in.")
        print("")
        print_desc("Someone is inside. Whoever is in there is not safe.")
        print_desc("I need to hurry and save them.")
        print_desc("But if I make too much noise... the killer might escape.")
        print_desc("I have to catch him this time.")
        print("")
        d.prevLocation = d.currentlocation
        d.currentlocation = "garden"
        handle_look()
        print("")
        return "no_clear"
    
    # truck
    if matchedPlace == "truck":
        print_desc("You walk to the truck. Its locked.")
        print_desc("The windows are tinted. You cant see inside.")
        return False
    
    # basement code
    if matchedPlace == "basement":
        # from hallway
        if loc == "hallway":
            print_action("You go down to the basement.")
            d.prevLocation = d.currentlocation
            d.currentlocation = "basement"
            return True
        # outside
        if d.basementUnlocked:
            print_action("You go inside the basement.")
            d.prevLocation = d.currentlocation
            d.currentlocation = "basement"
            return True
        elif "code paper" in d.inventory:
            print_action("The lock needs a 4-digit code.")
            codeInput = input("Enter code: ")
            if codeInput == d.basementCode:
                print_action("The door opens quietly. You go inside.")
                d.basementUnlocked = True
                d.prevLocation = d.currentlocation
                d.currentlocation = "basement"
                return True
            else:
                print_error("Wrong code. The lock stays closed.")
                return False
        else:
            print_desc("The door has a digital lock. You need to know the code.")
            return False
    
    # ladder
    if matchedPlace == "ladder":
        if d.ladderBroken:
            print_desc("You see the broken ladder on the ground.")
        d.prevLocation = d.currentlocation
        d.currentlocation = "ladder"
        return True
    
    # kitchen
    if matchedPlace == "kitchen":
        if d.kitchenUnlocked:
            d.prevLocation = d.currentlocation
            d.currentlocation = "kitchen"
            return True
        else:
            print_desc("The kitchen door is locked.")
            return False
    
    # dark basement exit
    if loc == "basement" and matchedPlace == "hallway":
        if not d.basementLightOn:
            print_desc("You move towards the stairs in the dark.")
            print_desc("You bump into a box. It falls over with a loud crash.")
            print_warning("You made a lot of noise.")
            d.escapeCounter = d.escapeCounter + 2
        else:
            print_desc("You turn off the flashlight.")
            print_desc("Using light inside the house would be too risky.")
        d.prevLocation = d.currentlocation
        d.currentlocation = "hallway"
        return True
    
    d.prevLocation = d.currentlocation
    d.currentlocation = matchedPlace
    return True


def handle_go_back():
    if d.prevLocation == "":
        print_error("You cant go back. This is where you started.")
        return False
    else:
        oldLoc = d.currentlocation
        d.currentlocation = d.prevLocation
        d.prevLocation = oldLoc
        return True


def handle_leave():
    loc = d.currentlocation
    
    # single exit rooms
    if loc == "car":
        # garden intro
        if d.firstTimeGarden:
            d.firstTimeGarden = False
            print_desc("You step out of your car.")
            print_desc("The fence gate is broken. Someone forced their way in.")
            print("")
            print_desc("Someone is inside. Whoever is in there is not safe.")
            print_desc("I need to hurry and save them.")
            print_desc("But if I make too much noise... the killer might escape.")
            print_desc("I have to catch him this time.")
            print("")
            d.prevLocation = loc
            d.currentlocation = "garden"
            handle_look()
            print("")
            return "no_clear"
        d.prevLocation = loc
        d.currentlocation = "garden"
        return True
    
    if loc == "salon":
        d.prevLocation = loc
        d.currentlocation = "hallway"
        return True
    
    if loc == "bedroom":
        d.prevLocation = loc
        d.currentlocation = "upstairs"
        return True
    
    if loc == "upstairs":
        d.prevLocation = loc
        d.currentlocation = "hallway"
        return True
    
    
    if loc == "ladder":
        d.prevLocation = loc
        d.currentlocation = "garden"
        return True
    
    if loc == "truck":
        d.prevLocation = loc
        d.currentlocation = "garden"
        return True
    
    print_error("I dont understand that command.")
    return False


def handle_take(item):
    loc = d.currentlocation
    roomItems = d.rooms[loc]["items"]
    
    matched = d.match_item(item, roomItems + d.inventory)
    
    # gun
    if matched == "gun":
        if matched in roomItems:
            d.inventory.append("gun")
            d.rooms[loc]["items"].remove("gun")
            print_action("You take the gun.")
            return True
        else:
            if "gun" in d.inventory:
                print_error("You already have that.")
            else:
                print_error("There is no gun here.")
            return False
    
    # flashlight
    if matched == "flashlight" or "flash" in item or "light" in item:
        if "flashlight" in roomItems:
            d.inventory.append("flashlight")
            d.rooms[loc]["items"].remove("flashlight")
            print_action("You take the flashlight.")
            return True
        else:
            if "flashlight" in d.inventory:
                print_error("You already have that.")
            else:
                print_error("There is no flashlight here.")
            return False
    
    # code paper
    if matched == "code paper":
        if matched in roomItems:
            d.inventory.append("code paper")
            d.rooms[loc]["items"].remove("code paper")
            print_action("You take the code paper.")
            return True
        else:
            print_error("You already have that.")
            return False
    
    # stick
    if matched == "stick" or "stick" in item:
        if "stick" in roomItems:
            d.inventory.append("stick")
            d.rooms[loc]["items"].remove("stick")
            print_desc("You grab the stick.")
            return True
        if "stick" in d.inventory:
            print_error("You already have that.")
            return False
        print_error("There is no stick here.")
        return False
    
    # key
    if matched == "key" or "key" in item:
        if "key" in roomItems:
            d.inventory.append("key")
            d.rooms[loc]["items"].remove("key")
            print_action("You got the key.")
            return True
        if "key" in d.inventory:
            print_error("You already have that.")
            return False
        print_error("There is no key here.")
        return False
    
    # bat
    if matched == "bat" or "bat" in item or "baseball" in item:
        if "bat" in roomItems:
            d.inventory.append("bat")
            d.rooms[loc]["items"].remove("bat")
            print_desc("You take the bat.")
            return True
        if "bat" in d.inventory:
            print_error("You already have that.")
            return False
        print_error("There is no bat here.")
        return False
    
    # golf club
    if matched == "golf club" or "golf" in item or "club" in item:
        if "golf club" in roomItems:
            d.inventory.append("golf club")
            d.rooms[loc]["items"].remove("golf club")
            print_desc("You grab the golf club.")
            return True
        if "golf club" in d.inventory:
            print_error("You already have that.")
            return False
        print_error("There is no golf club here.")
        return False
    
    # not here
    if matched not in roomItems and matched not in d.inventory:
        print_error("There is no " + item + " here.")
        return False
    
    print_error("You cant take that.")
    return False


def handle_open(item):
    loc = d.currentlocation
    roomItems = d.rooms[loc]["items"]
    
    matched = d.match_item(item, roomItems)
    
    # backseats
    if matched == "backseats" or "back" in item or "seat" in item:
        if "backseats" in roomItems:
            if d.backseatsChecked:
                if "gun" in roomItems:
                    print_desc("You already checked. There is a gun under the jacket.")
                else:
                    print_desc("You already checked. Nothing else there.")
                return False
            print_desc("You look at the backseats.")
            print_desc("Old jackets, empty coffee cups, papers...")
            print_desc("You notice something under a jacket. A gun.")
            d.rooms["car"]["items"].append("gun")
            d.backseatsChecked = True
            return True
        else:
            print_error("There are no backseats here.")
            return False
    
    # glove box
    if matched == "glove box" or "glove" in item or "box" in item:
        if "glove box" in roomItems:
            if d.gloveBoxOpen:
                if "flashlight" in roomItems:
                    print_desc("The glove box is open. There is a flashlight inside.")
                else:
                    print_desc("The glove box is empty.")
                return False
            print_desc("You open the glove box.")
            print_desc("There is a flashlight inside.")
            d.rooms["car"]["items"].append("flashlight")
            d.gloveBoxOpen = True
            return True
        else:
            print_error("There is no glove box here.")
            return False
    
    # doors
    if matched == "door" or "door" in item:
        if loc == "kitchen door":
            if d.kitchenUnlocked:
                print_desc("The door is already unlocked.")
                return False
            if "key" in d.inventory:
                print_action("You try the key. It fits! The door is now unlocked.")
                print_desc("Click. The door is now open.")
                d.kitchenUnlocked = True
                d.rooms["kitchen door"]["description"] = "You are at the back door. The door is unlocked. You can go inside."
                return True
            else:
                print_desc("The door is locked. You need a key.")
                return False
        if "door" in roomItems and loc == "front door":
            print_desc("You try the handle. Its locked.")
            print_desc("No way to get in through here.")
            d.triedFrontDoor = True
            return True
        print_error("There is no door to open here.")
        return False
    
    # lock
    if matched == "lock" or "lock" in item or "unlock" in item:
        return handle_use("lock")
    
    print_error("You cant open that.")
    return False


def handle_read(item):
    loc = d.currentlocation
    roomItems = d.rooms[loc]["items"]
    
    matched = d.match_item(item, roomItems + d.inventory)
    
    # code paper
    if matched == "code paper" or "paper" in item or "code" in item:
        if "code paper" in d.inventory:
            print_action("The paper says: " + d.basementCode)
            return True
        else:
            print_error("You dont have that.")
            return False
    
    # files
    if matched == "files" or "file" in item:
        if "files" in roomItems:
            print_action("You look at the files on the seat.")
            print_desc("The files contain information about a serial killer.")
            print_desc("He has been on the run for years. Many victims. All women.")
            print_desc("You have been chasing this man for a long time.")
            print_dialogue("\"I got you this time...\"")
            print_dialogue("\"All the clues point to this house. The next victim lives here.\"")
            print_dialogue("\"You must be here somewhere.\"")
            return True
        else:
            print_error("There are no files here.")
            return False
    
    print_error("You cant read that.")
    return False


def handle_use(item):
    loc = d.currentlocation
    roomItems = d.rooms[loc]["items"]
    
    matched = d.match_item(item, roomItems + d.inventory)
    
    # paper
    if "paper" in item or matched == "code paper":
        if "code paper" in d.inventory:
            print_action("The paper says: " + d.basementCode)
            return True
        else:
            print_error("You dont have that.")
            return False
    
    # files
    if "file" in item or matched == "files":
        return handle_read(item)
    
    # glove box
    if "box" in item or matched == "glove box":
        return handle_open(item)
    
    # flashlight
    if "flash" in item or "light" in item or matched == "flashlight":
        if "flashlight" in d.inventory:
            if loc == "basement":
                if d.basementLightOn:
                    print_desc("The flashlight is already on.")
                    return False
                print_desc("You turn on the flashlight.")
                print_desc("The basement lights up. You see old furniture and boxes. A baseball bat leans against the wall.")
                d.basementLightOn = True
                return True
            else:
                print_desc("You dont need the flashlight here.")
                return False
        else:
            print_error("You dont have a flashlight.")
            return False
    
    # ladder
    if "ladder" in item or matched == "ladder":
        if d.ladderBroken:
            print_desc("The ladder is broken. Just pieces of wood on the ground now.")
            return False
        if "ladder" in roomItems:
            print_desc("You grab the ladder and start climbing...")
            print_desc("The wood breaks.")
            print_desc("The old wood breaks under your weight. You fall to the ground.")
            print_desc("Pain shoots through your ankle. You sprained it.")
            print_desc("The noise echoes in the quiet night.")
            d.ladderBroken = True
            d.escapeCounter = d.escapeCounter + 2
            if "ladder" in d.rooms["ladder"]["items"]:
                d.rooms["ladder"]["items"].remove("ladder")
                d.rooms["ladder"]["items"].append("broken ladder")
            d.rooms["ladder"]["description"] = "You stand where the ladder used to be. Broken pieces of wood are scattered on the ground. Your ankle hurts."
            return True
        else:
            print_error("There is no ladder here.")
            return False
    
    # mat
    if matched == "mat" or "mat" in item:
        if "mat" in roomItems:
            print_action("You lift the mat.")
            print_action("You find a small paper with a 4-digit code: " + d.basementCode)
            d.inventory.append("code paper")
            d.rooms["front door"]["items"].remove("mat")
            d.rooms["front door"]["items"].append("lifted mat")
            print_action("You put the code paper in your pocket.")
            return True
        elif "lifted mat" in roomItems:
            print_warning("You already looked under the mat.")
            return False
        else:
            print_error("There is no mat here.")
            return False
    
    # bell
    if matched == "bell" or "bell" in item:
        if "bell" in roomItems:
            if d.rangBell:
                print_desc("You already rang the doorbell. No one answered.")
                return False
            print_desc("You reach for the doorbell...")
            print_action("Are you sure? This could alert someone inside. (y/n)")
            confirm = input("> ").lower().strip()
            if confirm == "y" or confirm == "yes":
                print_desc("You press the doorbell.")
                print_desc("DING DONG. Its really loud.")
                print_desc("You wait. No one answers.")
                print_desc("But you notice the light in the upstairs window flicker.")
                d.rangBell = True
                d.escapeCounter = d.escapeCounter + 4
                return True
            else:
                print_desc("You pull your hand back. Better not.")
                return False
        else:
            print_error("There is no bell here.")
            return False
    
    # lock
    if matched == "lock" or "lock" in item:
        if "lock" in roomItems:
            if d.basementUnlocked:
                print_desc("The lock is already open.")
                return False
            if "code paper" in d.inventory:
                print_desc("You look at the digital lock.")
                codeInput = input("Enter code: ")
                if codeInput == d.basementCode:
                    print_desc("Click. The lock opens.")
                    d.basementUnlocked = True
                    return True
                else:
                    print_desc("Nothing happens. Wrong code.")
                    return False
            else:
                print_desc("You examine the lock. It needs a 4-digit code.")
                print_desc("You dont know what the code is.")
                return False
        else:
            print_error("There is no lock here.")
            return False
    
    # gun
    if matched == "gun" or "gun" in item:
        if "gun" in d.inventory:
            print_warning("You hold the gun ready. But there is nothing to shoot here.")
            return False
        else:
            print_error("You dont have a gun.")
            return False
    
    # stick
    if matched == "stick" or "stick" in item:
        if "stick" in d.inventory:
            if loc == "back garden" and not d.birdhouseDown:
                print_action("You pushed the bird house with the stick.")
                print_desc("The birdhouse falls and breaks on the ground.")
                print_desc("It makes a lot of noise.")
                print_action("Something shiny falls out. Its a key!")
                d.birdhouseDown = True
                d.escapeCounter = d.escapeCounter + 2
                d.rooms["back garden"]["items"].append("key")
                if "birdhouse" in d.rooms["back garden"]["items"]:
                    d.rooms["back garden"]["items"].remove("birdhouse")
                    d.rooms["back garden"]["items"].append("broken birdhouse")
                d.rooms["back garden"]["description"] = "You are in the back garden. The broken birdhouse lies on the ground under the tree. A key is here. A door leads to the kitchen."
                return True
            elif d.birdhouseDown:
                print_warning("There is nothing to use the stick at.")
                return False
            else:
                print_warning("You wave the stick around. Nothing happens.")
                return False
        else:
            print_error("You dont have a stick.")
            return False
    
    # birdhouse
    if matched == "birdhouse" or "bird" in item:
        if d.birdhouseDown:
            print_desc("The birdhouse is broken on the ground.")
            return False
        else:
            print_desc("The birdhouse is too high. You cant reach it.")
            return False
    
    print_error("You cant use that here.")
    return False


def handle_inventory():
    if d.inventory:
        print_action("You have: " + ", ".join(d.inventory))
    else:
        print_action("Your pockets are empty.")


def handle_save():
    d.save_data()
    print_action("Game saved!")


def handle_quit():
    print_action("Do you want to save before quitting? (y/n)")
    choice = input("> ")
    if choice.lower() == "y":
        d.save_data()
        print_action("Game saved!")
    print_action("Goodbye detective...")
    sys.exit()
