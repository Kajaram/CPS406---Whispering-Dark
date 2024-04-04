from Functions.locationFunctions import get_location

def move_player(command, current_location, locations, inventory):

    if  command == "north" and current_location['id']=="church-entrance" and "basement_key" not in inventory:
        print("The door is locked.")
        return current_location, False
    
    elif command == "north" and current_location['id']=="cabin" and "flashlight" not in inventory:
        print("The path is too dark and treachurous to pass.\nWe need something to light the way..")
        return current_location, False
    

    elif command in current_location.get('exits', {}):
        new_location_id = current_location['exits'][command]
        return get_location(new_location_id, locations), True
    
    else:
        print("You can't move in that direction..")
        return current_location, False