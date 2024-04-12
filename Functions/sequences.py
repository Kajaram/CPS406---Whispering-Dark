import json
from Functions.engine import set_event_happened, check_event_happened
from Functions.fight import fightFunc
from Functions.centerprint import centered_print

def cutscene(file_path, sequence):
    with open(file_path, 'r') as file:
        game_data = json.load(file)
        for event in game_data['world']['events']:
            if event['id'] == sequence:
                return event['sentences']
        return []

def sequence(sequenceName, events, player='', enemy='', dialogue='', items=''):


    if sequenceName == 'book':
        intro_cutscene_sentences = cutscene('Whispering-Dark Updated.json', sequenceName) 
        print("\nPress Enter to display the next line of text")
        print("\nEnter 's' to skip")
        for sentence in intro_cutscene_sentences:
            centered_print(sentence)
            user_input = input()
            if user_input.lower() == 's':
                break

        set_event_happened(sequenceName, events)

    elif not check_event_happened(sequenceName, events):
        intro_cutscene_sentences = cutscene('Whispering-Dark Updated.json', sequenceName) 
        print("\nPress Enter to display the next line of text")
        print("\nEnter 's' to skip")
        for sentence in intro_cutscene_sentences:
            print(sentence)
            user_input = input()
            if user_input.lower() == 's':
                set_event_happened(sequenceName, events)
                break

        set_event_happened(sequenceName, events)
        
        if (sequenceName) == 'basement_confrontation' or sequenceName == 'wendigo_confrontation':
            fightFunc(player, enemy, dialogue, items)
        
        elif (sequenceName) == 'radio_tower':
            print("\n\nCongratulations! help is on its way.\nYou survived the clutches of the evil cultists and the wendigo.\nFeel free to explore or type 'quit' to exit.")
            input("\nPress enter to continue...")

    