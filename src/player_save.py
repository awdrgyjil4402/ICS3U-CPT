import json 
import os

player_settings = {
    'username': 'deafqnd', 
    'health': 3, 
    'level': 1, 
    'inventory': ['lightning_sword', 'rage_potion']
}

# Save the Progress
def save_player(data, filename='savegame.json'):
    # Saves player info to json
    try: 
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Game saved to {filename}")
    except IOError as e:
        print(f"Error saving file: {e}")

# Load Progress

def load_player(filename="savegame.json", default_data=None):

    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                print(f"Game loaded from {filename}")
                return data

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            player_default = {
            'username': 'default', 
            'health': 3, 
            'level': 0,
            'inventory': ['sword', 'health_potion']
            }
            return player_default

        except FileNotFoundError:
            print(f"No save file found ({filename}), starting a new game.")
            player_default = {
            'username': 'default', 
            'health': 3, 
            'level': 0,
            'inventory': ['sword', 'health_potion']
            }
            return player_default
    
    else:
        print('Settings file not found. Using defaults')
        player_default = {
        'username': 'default', 
        'health': 3, 
        'level': 0,
        'inventory': ['sword', 'health_potion']
        }
        return player_default


# EXAMPLE USES

# loaded_player_data = load_player(default_data = player_default)
# print('Loaded player data')

# player_settings['username'] = 'deafqnd'
# player_settings['level'] = 3

# save_player(player_settings)
