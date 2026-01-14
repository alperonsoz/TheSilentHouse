import os
import sys
from print_text import *
import data as d
import commands as cmd

# game

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


clear_screen()
print_title("THE SILENT HOUSE")
print("")


print_action("Do you want to load a previous save? (y/n)")
loadChoice = input("> ")

while loadChoice.lower() not in ["y", "n", "yes", "no"]:
    loadChoice = input("> ")

if loadChoice.lower() in ["y", "yes"]:
    if d.load_data():
        print_action("Game loaded!")
    else:
        print_warning("Starting new game...")

print("")
print_desc("Type -help if you need help")
print("")


cmd.handle_look()
print("")

# loop
gameRunning = True

while gameRunning:

    print_action("What's your next move?")
    action = input("> ").lower().strip()
    
    # max 3 words
    words = action.split()
    if len(words) > 3:
        print_error("Too many words. Use simple commands like: go garden, take stick")
        continue
    
    # item/place check
    isCommand = False
    commandList = ["go ", "take ", "open ", "read ", "use ", "unlock ", "look", "inventory", "inv", "save", "quit", "-help", "go back", "leave car"]
    for c in commandList:
        if action.startswith(c) or action == c.strip():
            isCommand = True
            break
    
    # what to do
    if not isCommand and action != "":
        foundItem = d.check_if_item(action)
        foundPlace = d.check_if_place(action)
        
        if foundItem != None:
            print_action("What do you want to do with the " + foundItem + "?")
            answer = input("> ").lower().strip()
            action = answer + " " + foundItem
        elif foundPlace != None:
            print_action("What do you want to do with " + foundPlace + "?")
            answer = input("> ").lower().strip()
            if answer == "go" or answer == "enter" or answer == "walk":
                action = "go " + foundPlace
            else:
                action = answer + " " + foundPlace
    
    # commands
    if action == "-help":
        print("")
        print_help()
    
    elif action == "look":
        print("")
        cmd.handle_look()
        print("")
    
    elif action.startswith("look "):
        target = action[5:]
        if "back" in target or "seat" in target:
            cmd.handle_open(target)
        else:
            print_error("Just type: look")
    
    elif action == "go back":
        result = cmd.handle_go_back()
        if result:
            if d.insideHouse and d.currentlocation != "bedroom":
                d.escapeCounter = d.escapeCounter + 1
            clear_screen()
            cmd.handle_look()
            print("")
            # tension
            if d.insideHouse and d.escapeCounter < 9:
                if d.escapeCounter == 4:
                    print_warning("You hear footsteps above you.")
                    print("")
                elif d.escapeCounter == 6:
                    print_warning("You hear some sounds from the bedroom.")
                    print("")
                elif d.escapeCounter == 7:
                    print_warning("You hear a woman whimpering.")
                    print("")
    
    elif action == "leave" or action == "leave car":
        result = cmd.handle_leave()
        if result == "no_clear":
            # no clear
            pass
        elif result:
            if d.insideHouse and d.currentlocation != "bedroom":
                d.escapeCounter = d.escapeCounter + 1
            clear_screen()
            cmd.handle_look()
            print("")
            # tension
            if d.insideHouse and d.escapeCounter < 9:
                if d.escapeCounter == 4:
                    print_warning("You hear footsteps above you.")
                    print("")
                elif d.escapeCounter == 6:
                    print_warning("You hear some sounds from the bedroom.")
                    print("")
                elif d.escapeCounter == 7:
                    print_warning("You hear a woman whimpering.")
                    print("")
    
    elif action.startswith("go "):
        place = action[3:]
        result = cmd.handle_go(place)
        if result == "no_clear":
            # no clear
            pass
        elif result:
            if d.insideHouse and d.currentlocation != "bedroom":
                d.escapeCounter = d.escapeCounter + 1
            clear_screen()
            cmd.handle_look()
            print("")
            # tension
            if d.insideHouse and d.escapeCounter < 9:
                if d.escapeCounter == 4:
                    print_warning("You hear footsteps above you.")
                    print("")
                elif d.escapeCounter == 6:
                    print_warning("You hear some sounds from the bedroom.")
                    print("")
                elif d.escapeCounter == 7:
                    print_warning("You hear a woman whimpering.")
                    print("")
    
    elif action.startswith("take "):
        item = action[5:]
        cmd.handle_take(item)
    
    elif action.startswith("open "):
        item = action[5:]
        cmd.handle_open(item)
    
    elif action.startswith("read "):
        item = action[5:]
        cmd.handle_read(item)
    
    elif action.startswith("use "):
        item = action[4:]
        cmd.handle_use(item)
    
    elif action.startswith("unlock "):
        item = action[7:]
        cmd.handle_open(item)
    
    elif action == "inventory" or action == "inv":
        cmd.handle_inventory()
    
    elif action == "save":
        cmd.handle_save()
    
    elif action == "quit":
        cmd.handle_quit()
    
    else:
        print_error("I dont understand that command.")
    
    
    # inside house check
    if d.currentlocation in ["kitchen", "basement", "hallway", "bedroom", "salon", "upstairs"]:
        if not d.insideHouse:
            d.insideHouse = True
    
    
    # too late ending
    if d.escapeCounter >= 9:
        import time
        print("")
        print_warning("You hear a scream.")
        time.sleep(2)
        print_desc("Then nothing. Only silence.")
        print("")
        time.sleep(1)
        print_desc("You run to the bedroom.")
        time.sleep(1)
        print_desc("The window is open. The room is cold.")
        time.sleep(1)
        print_desc("There is a woman on the bed. She is covered in blood.")
        time.sleep(1)
        print_desc("You are too late. She is dead and the killer has escaped.")
        print("")
        time.sleep(1)
        print_title("BAD ENDING - TOO LATE")
        gameRunning = False
    
    # combat
    if d.currentlocation == "bedroom" and d.escapeCounter < 9:
        import random
        import time
        
        print("")
        print_title("CONFRONTATION")
        print_desc("The killer turns around. He has a knife.")
        print_desc("The woman is on the bed, crying. She is still alive.")
        print("")
        
        combatRunning = True
        combatTurn = 0
        killerStunned = False
        hits = 0
        killerHits = 0
        
        while combatRunning:
            combatTurn = combatTurn + 1
            
            
            if killerStunned:
                print_warning("The killer is off balance!")
                print_action("Now is your chance! (use [weapon])")
                
                # get valid input
                validInput = False
                while not validInput:
                    playerAction = input("> ").lower().strip()
                    
                    # inventory check
                    if playerAction == "inv" or playerAction == "inventory":
                        print("")
                        if len(d.inventory) == 0:
                            print_desc("Your inventory is empty.")
                        else:
                            print_desc("You have: " + ", ".join(d.inventory))
                        print("")
                        print_action("Now is your chance! (use [weapon])")
                        continue
                    
                    if "use" in playerAction:
                        validInput = True
                    else:
                        print_error("(use [weapon])")
                        continue
                
                # gun while stunned
                if "gun" in playerAction and "gun" in d.inventory:
                    print_action("You aim your gun at the killer.")
                    print("")
                    print_action("Where do you want to shoot? (head / shoulder)")
                    shot = input("> ").lower().strip()
                    
                    if "head" in shot:
                        print("")
                        print_desc("You shoot.")
                        time.sleep(1)
                        print_desc("He falls. He is dead.")
                        time.sleep(1)
                        print_desc("The woman is safe. But you killed him.")
                        print("")
                        time.sleep(1)
                        print_title("DARK ENDING - KILLER DEAD")
                    else:
                        print("")
                        print_desc("You shoot.")
                        time.sleep(1)
                        print_desc("He screams, drops the knife.")
                        print_action("You handcuff him.")
                        time.sleep(1)
                        print_desc("The woman is safe. The killer will go to jail.")
                        print("")
                        time.sleep(1)
                        print_title("GOOD ENDING - JUSTICE SERVED")
                    combatRunning = False
                    gameRunning = False
                
                # bat while stunned
                elif ("bat" in playerAction or "baseball" in playerAction) and "bat" in d.inventory:
                    print_action("You swing the bat at his head.")
                    killerHits = killerHits + 1
                    if killerHits >= 2:
                        time.sleep(1)
                        print_desc("He falls down.")
                        time.sleep(1)
                        print_action("You handcuff him.")
                        print_desc("The woman is safe. The killer will go to jail.")
                        print("")
                        time.sleep(1)
                        print_title("GOOD ENDING - JUSTICE SERVED")
                        combatRunning = False
                        gameRunning = False
                    else:
                        print_desc("He stumbles back.")
                        killerStunned = False
                        print("")
                
                # golf club while stunned
                elif ("golf" in playerAction or "club" in playerAction) and "golf club" in d.inventory:
                    print_action("You swing the club at his head.")
                    killerHits = killerHits + 1
                    if killerHits >= 2:
                        time.sleep(1)
                        print_desc("He falls down.")
                        time.sleep(1)
                        print_action("You handcuff him.")
                        print_desc("The woman is safe. The killer will go to jail.")
                        print("")
                        time.sleep(1)
                        print_title("GOOD ENDING - JUSTICE SERVED")
                        combatRunning = False
                        gameRunning = False
                    else:
                        print_desc("He stumbles back.")
                        killerStunned = False
                        print("")
                
                # fist while stunned
                elif "fist" in playerAction or "punch" in playerAction:
                    print_action("You punch him in the face")
                    killerHits = killerHits + 1
                    if killerHits >= 4:
                        time.sleep(1)
                        print_desc("He falls down, dazed.")
                        time.sleep(1)
                        print_action("You handcuff him.")
                        print_desc("The woman is safe. The killer will go to jail.")
                        print("")
                        time.sleep(1)
                        print_title("GOOD ENDING - JUSTICE SERVED")
                        combatRunning = False
                        gameRunning = False
                    else:
                        print_desc("He stumbles back.")
                        killerStunned = False
                        print("")
                
                else:
                    print_error("You dont have that weapon!")
                    killerStunned = False
                continue
            
            # killer action
            if combatTurn > 5:
                killerAction = "attack"
            else:
                killerAction = random.choice(["attack", "wait"])
            
            if killerAction == "attack":
                print_warning("The killer attacks you with his knife!")
            else:
                print_desc("The killer watches you carefully.")
            
            print("")
            print_action("What do you do? (dodge / use [weapon] / wait)")
            
            # get valid input
            validInput = False
            while not validInput:
                playerAction = input("> ").lower().strip()
                
                # inventory check
                if playerAction == "inv" or playerAction == "inventory":
                    print("")
                    if len(d.inventory) == 0:
                        print_desc("Your inventory is empty.")
                    else:
                        print_desc("You have: " + ", ".join(d.inventory))
                    print("")
                    print_action("What do you do? (dodge / use [weapon] / wait)")
                    continue
                
                # cant leave
                if "leave" in playerAction or playerAction.startswith("go ") or playerAction == "go":
                    print_error("You can't leave now!")
                    continue
                
                # valid actions
                if "dodge" in playerAction or "wait" in playerAction or "use" in playerAction:
                    validInput = True
                else:
                    print_error("(dodge / use [weapon] / wait)")
                    continue
            
            # dodge
            if "dodge" in playerAction:
                if killerAction == "attack":
                    print_action("You jump to the side. The knife misses.")
                    print_desc("He loses balance.")
                    killerStunned = True
                    print("")
                else:
                    print_desc("You move but he doesn't attack.")
                    print("")
            
            # wait
            elif "wait" in playerAction:
                if killerAction == "attack":
                    hits = hits + 1
                    if hits >= 2:
                        print("")
                        print_title("YOU DIED")
                        time.sleep(1)
                        print_desc("The knife goes through you, you fall unconscious..")
                        print("")
                        time.sleep(1)
                        print_title("BAD ENDING - DETECTIVE DIED")
                        combatRunning = False
                        gameRunning = False
                    else:
                        print_warning("The knife cuts your arm. It hurts.")
                        print_desc("You feel dizzy.")
                        print("")
                else:
                    print_desc("Nothing happens. You both just stand there.")
                    print("")
            
            # use weapon
            elif "use" in playerAction:
                if killerAction == "attack":
                    hits = hits + 1
                    if hits >= 2:
                        print("")
                        print_title("YOU DIED")
                        time.sleep(1)
                        print_desc("You were too slow. The knife cuts through you.")
                        print("")
                        time.sleep(1)
                        print_title("BAD ENDING - DETECTIVE DIED")
                        combatRunning = False
                        gameRunning = False
                    else:
                        print_warning("He cuts you before you can swing.")
                        print_desc("It hurts. There is blood on your shirt.")
                        print("")
                else:
                    # gun
                    if "gun" in playerAction:
                        if "gun" in d.inventory:
                            print_action("You aim your gun at the killer.")
                            print("")
                            print_action("Where do you shoot? (head / shoulder)")
                            shot = input("> ").lower().strip()
                            
                            if "head" in shot:
                                print("")
                                print_desc("You shoot.")
                                time.sleep(1)
                                print_desc("He falls. Dead.")
                                time.sleep(1)
                                print_desc("The woman is safe. But you killed him.")
                                print("")
                                time.sleep(1)
                                print_title("DARK ENDING - KILLER DEAD")
                            else:
                                print("")
                                print_desc("You shoot.")
                                time.sleep(1)
                                print_desc("He screams and drops the knife.")
                                print_action("You handcuff him.")
                                time.sleep(1)
                                print_desc("The woman is safe. The killer will go to jail.")
                                print("")
                                time.sleep(1)
                                print_title("GOOD ENDING - JUSTICE SERVED")
                            
                            combatRunning = False
                            gameRunning = False
                        else:
                            print_error("You dont have a gun!")
                    
                    # bat
                    elif "bat" in playerAction or "baseball" in playerAction:
                        if "bat" in d.inventory:
                            print_action("You swing the bat at the killer!")
                            killerHits = killerHits + 1
                            if killerHits >= 2:
                                print_desc("You hit him.")
                                time.sleep(1)
                                print_desc("He falls down.")
                                time.sleep(1)
                                print_action("You handcuff him.")
                                print_desc("The woman is safe. The killer will go to jail.")
                                print("")
                                time.sleep(1)
                                print_title("GOOD ENDING - JUSTICE SERVED")
                                combatRunning = False
                                gameRunning = False
                            else:
                                print_desc("You hit him. He stumbles back.")
                                print("")
                        else:
                            print_error("You dont have a bat!")
                    
                    # golf club
                    elif "golf" in playerAction or "club" in playerAction:
                        if "golf club" in d.inventory:
                            print_action("You swing the golf club at the killer!")
                            killerHits = killerHits + 1
                            if killerHits >= 2:
                                print_desc("You hit him.")
                                time.sleep(1)
                                print_desc("He falls down.")
                                time.sleep(1)
                                print_action("You handcuff him.")
                                print_desc("The woman is safe. The killer will go to jail.")
                                print("")
                                time.sleep(1)
                                print_title("GOOD ENDING - JUSTICE SERVED")
                                combatRunning = False
                                gameRunning = False
                            else:
                                print_desc("You hit him. He stumbles back.")
                                print("")
                        else:
                            print_error("You dont have a golf club!")
                    
                    # fist
                    elif "fist" in playerAction or "punch" in playerAction:
                        print_action("You throw a punch at the killer!")
                        killerHits = killerHits + 1
                        if killerHits >= 4:
                            print_desc("You hit him hard.")
                            time.sleep(1)
                            print_desc("He is dizzy. He falls down.")
                            time.sleep(1)
                            print_action("You handcuff him.")
                            print_desc("The woman is safe. The killer will go to jail.")
                            print("")
                            time.sleep(1)
                            print_title("GOOD ENDING - JUSTICE SERVED")
                            combatRunning = False
                            gameRunning = False
                        else:
                            print_desc("You hit him. He stumbles back.")
                            print("")
                    
                    else:
                        print_error("Use what?")

print("")
print_action("Press Enter to exit...")
input()
