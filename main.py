from Functions.locationFunctions import get_location, describe_location
from Functions.movement import move_player
from Functions.inventoryFunctions import pick_up_item, use_item
from Functions.engine import load_game_data,check_event_happened, set_event_happened
from Functions.intro import sequence
from Functions.quickTime import timer
from Objects.Character import Character
from Functions.fight import fightFunc
from Functions.open import openItem
from Functions.save_system import save_game, load_game
from Functions.mainMenu import mainMenu
import os
import time
# import sys
# sys.path.append('c:\python312\lib\site-packages')

locations = load_game_data('assets/Whispering-Dark Updated.json', 'locations') 
events = load_game_data('assets/Whispering-Dark Updated.json', 'events') 
dialogue = load_game_data('assets/Whispering-Dark Updated.json', 'dialogue') 
items = load_game_data('assets/Whispering-Dark Updated.json', 'items') 
current_location = get_location('cabin', locations) 

player = Character(100, 'player')
wendigo = Character(200, 'wendigo', 40)
cultist = Character(30, 'cultist', 30)

cultist.setCustomName = 'cultist'
wendigo.setCustomName = 'wendigo'


evelyn = Character(50)
sophia = Character(100)
rohan = Character(100)
ava = Character(100)
daniel = Character(100)


# Main game loop
if __name__ == '__main__':


    loaded = mainMenu(player, locations, wendigo, cultist, events, current_location)

    if not loaded:
        myName = input('\nEnter your Name:\n\n')
        print("\nWelcome,", myName)
        input("\nPress enter...\n")
        player.setCustomName(myName)
        os.system('cls' if os.name == 'nt' else 'clear')
        sequence('intro_cutscene', events, player, cultist, dialogue, items)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nWelcome to Whispering Dark. \nType 'quit' to exit at any time and 'pause' for the menu.")
        input("\n\nPress enter to continue...")

    else:
        loaded_state = load_game()
        player.from_dict(loaded_state["player"])
        wendigo.from_dict(loaded_state["wendigo"])
        cultist.from_dict(loaded_state["cultist"])
        events = loaded_state["events"]
        current_location = get_location(loaded_state["current_location_id"], locations)
        
    os.system('cls' if os.name == 'nt' else 'clear')


    while True:

        os.system('cls' if os.name == 'nt' else 'clear')

        describe_location(current_location)
        # print(current_location['items'])
        command = input("\nWhat do you want to do?\n").strip().lower()
        command = command.split()
        
        
        if len(command) > 0:
            if command[0] == 'quit':
                print(f"Thanks for playing {player.getCustomName()}. Goodbye!")
                time.sleep(3)
                # os.system('cls')
                break

            elif command[0] == 'pause':
                 mainMenu(player, locations, wendigo, cultist, events, current_location)

            
            elif command[0] == 'inventory':
                player.showInventory()
                input("\nPress enter to continue...")

            elif command[0] in ['move', 'go', 'walk', 'travel','run']:
                current_location, moved = move_player(command[1], current_location, locations, player.getInventory())
                
                if not moved:
                    input("\nPress enter to continue...")
                else:

                    if current_location['id'] == 'trail' and not wendigo.checkIsDead() and 'axe' in player.getInventory():
                        
                        sequence('wendigo_confrontation', events, player, wendigo, dialogue, items)
                      
                        

                    elif current_location['id'] == 'church_entrance':

                        sequence('church_discovery', events, player, cultist, dialogue, items)   



                    elif current_location['id'] == 'church_basement' and not cultist.checkIsDead():

                        sequence('basement_confrontation', events, player, cultist, dialogue, items)
                        
                    elif current_location['id'] == 'radio_tower':

                        sequence('radio_tower', events, player, player, dialogue, items)
                        

                    else:    
                        continue

                if player.checkIsDead() :
                        print(f"Thanks for playing {player.getCustomName()}. Goodbye!")
                        break
        

            elif command[0] in ['grab', 'take', 'equip'] :
                pick_up_item(command[1], player.getInventory(), current_location, player)

            elif command[0] in ['open', 'unlock', 'read']:
                openItem(current_location, player.getInventory(), command[1], player)

            elif command[0] in ['use']:
                use_item(command[1], current_location ,player.getInventory(), player, events)

            else:
                print("\nUnknown command. Please try again.")
                time.sleep(2)

        else:
            print("\nPlease enter a command..")
            time.sleep(2)
