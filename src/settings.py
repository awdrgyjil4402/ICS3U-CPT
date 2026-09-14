import json 
import os

settings_data = {
    "theme": "light",
    'volume': 20,
    'keybinds': 'wasd',
}

def save_settings(data, filename="settings.json"):
    try: 
        with open(filename, "w") as f:
            json.dump(data, f, indent=4) 
            # ^^^ indent for human-readable format
    except IOError as e:
        print(f'Error saving file: {e}')

# Loading settings from JSON

def load_settings(filename="settings.json", default_settings=None):

    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')
            default_settings = {
            'theme': 'light',
            'volume': 50,
            'keybinds': 'wasd' 
            }
            return default_settings
        except IOError as e:
            print(f"Error reading file: {e}")
            default_settings = {
            'theme': 'light',
            'volume': 50,
            'keybinds': 'wasd' 
            }
            return default_settings

    else: 
        print('Settings file not found. Using defaults')
        default_settings = {
        'theme': 'light',
        'volume': 50,
        'keybinds': 'wasd' 
        }
        return default_settings

settings_data['keybinds'] = 'arrows'

save_settings(settings_data)
# EXAMPLE USES

# Updatings and Saving Settings

# Load existing settings
# app_settings = load_settings(default_settings = default_settings)
# print(f"Current theme: {app_settings['theme']}")

# Update a setting
# settings_data['username'] = 'deafqnd'
# settings_data['volume'] = 16

# # Save the updated settings
# save_settings(settings_data)
