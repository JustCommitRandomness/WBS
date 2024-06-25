import json
import os
import sys
from worldbuilding import (
    add_universe, get_universe_details,
    list_galaxies, list_worlds, list_stories,
    init_galaxy, init_world, init_story, commit_changes
)

def booboo(string):
    print(string)
    
config_data = {}
universes_details = {}
state_data = {}

global_options = ['s','c','u','d']
def global_choice(choice):
    if choice == 's':
        print_state(state_data)
    elif choice == 'c':
        print_config(config_data)
    elif choice == 'u':
        print_state(universes_details)
            
def print_state(state):
    print(json.dumps(state, indent=4))

def print_config(config_data):
    print(json.dumps(config_data, indent=4))

def get_state_filename(config_file):
    return config_file + ".state"

def load_state(state_file):
    if os.path.exists(state_file):
        with open(state_file, 'r') as file:
            s = json.load(file)
    else:
        print("booboo")
        s = {}
    #ensure expectations aremet
    for dict in ["levels","locations"]:
        if not dict in s:
            s[dict] = {}

    return s

def save_state(state, state_file):
    with open(state_file, 'w') as file:
        json.dump(state, file, indent=4)

def manage_authors_and_voices(config_file):
    config_data = load_config(config_file)
    print("Manage Authors and Voices:")
    author = input("Enter author name: ")
    voices = input("Enter voices (comma-separated): ").split(',')
    config_data["authors"][author] = {
        "voices": voices
    }
    save_config(config_file, config_data)
    print(f"Updated author {author} with voices {voices}")

def get_current_location(state, universe):
    location = state.get("locations", {}).get(universe, {})
    location_parts = [universe]
    galaxy = location.get("current_galaxy")
    world = location.get("current_world")
    story = location.get("current_story")
    
    if galaxy and (galaxy != "_default_galaxy" or len(location.get("galaxies", [])) > 1):
        location_parts.append(galaxy)
    if world:
        location_parts.append(world)
    if story:
        location_parts.append(story)
    
    return " > ".join(location_parts)

def update_current_location(state, universe, key, value):
    if "locations" not in state:
        state["locations"] = {}
    if universe not in state["locations"]:
        state["locations"][universe] = {}
    state["locations"][universe][key] = value

def main_menu(config_file):
    while True:
        universes = [u['name'] for u in config_data.get('universes', [])]
        
        print("Worldbuilding System Main Menu:")

        universe_name = None
        if "current_universe" in state_data:
            def_universe = state_data["current_universe"]
        elif len(universes) == 1:
            def_universe = universes[0]
        else:
            def_universe = None

        if def_universe:
            if len(universes) == 1 and def_universe.startswith("_"):
                universe_name = None
            else:
                universe_name = def_universe
        
        print(f"+. Return to {universe_name} Universe")

        for i, universe in enumerate(universes):
            print(f"{i + 1}. Enter Universe: {universe}")

        print(f"{len(universes) + 1}. Add Universe")
        print(f"{len(universes) + 2}. Manage Authors and Voices")
        print(f"{len(universes) + 3}. Commit Changes")
        print("0. Exit")

        choice = input("Enter your choice: ")
        
        if choice in global_options:
            global_choice(choice)
        elif choice == '+' and ("current_universe" in state or len(universes) == 1):
            if len(universes) == 1:
                state["current_universe"] = universes[0]
            navigate_worldbuilding_space()
        elif 1 <= int(choice) <= len(universes):
            universe_choice = int(choice) - 1
            state_data["current_universe"] = universes[universe_choice]
            navigate_worldbuilding_space()
        elif choice == str(len(universes) + 1):
            universe_repo = input("Enter path for the new universe: ")
            author = input("Enter author name: ")
            add_universe(universe_repo, author)
        elif choice == str(len(universes) + 2):
            manage_authors_and_voices(config_file)
        elif choice == str(len(universes) + 3):
            repo_path = next((universe["repo"] for universe in load_config(config_file)["universes"] if universe["name"] == state.get("current_universe")), None)
            if repo_path:
                commit_changes(repo_path)
        elif choice == '0':
            save_state(state_data, state_file)
            print("Exiting...")
            return
        else:
            print("Invalid choice, please try again.")

        save_state(state_data, state_file)

def navigate_worldbuilding_space():
    levels = ["universe", "galaxy", "world", "story"]
    current_universe = state_data["current_universe"]
    if not (universe_repo := universes_details[current_universe]):
        booboo("something is wrong in the universe")
        return
    state_data["current_level"] = \
        state_data["levels"].get(current_universe, levels[0])
    
    current_location = state_data["locations"].get(current_universe, {})

    while True:
        current_level = state_data["current_level"]
        level_index = levels.index(current_level)
        
        down_level = levels[level_index + 1] if len(levels) > level_index + 1 \
               else current_level
        up_level = levels[level_index - 1] if 0 < level_index \
               else current_level
        level = current_level.capitalize()
        print(f"{level} Level Actions:")
        print(f"r. Rename {level}")
        print(f"x. Delete {level}")
        print(f"a. add {down_level}")
        print(f"-. Move Up to {up_level} Level")
        print(f"+. Move Down to {down_level} Level")
        print("0. Back to Main Menu")
        print("*. Return to System Menu")

        choice = input("Enter your choice: ")

        if choice in global_options:
            global_choice(choice)
        elif choice == 'r':
            new_name = input(f"Enter new name for the {current_level}: ")
            os.rename(os.path.join(universe_repo, f"{current_level}s", current_name), os.path.join(universe_repo, f"{current_level}s", new_name))
            update_current_location(state, current_universe, f"current_{current_level}", new_name)
        elif choice == 'x':
            os.rmdir(os.path.join(universe_repo, f"{current_level}s", current_name))
            update_current_location(state, current_universe, f"current_{current_level}", None)
        elif choice == '3':
            path = input(f"Enter path for the new {lower_level}: ")
            commit_message = f"Add {lower_level} {os.path.basename(path)}"
            eval("add_"+down_level)(universe_repo, current_name, path, author, commit_message)
            print(f"{lower_level.capitalize()} {os.path.basename(path)} added. Commit message: {commit_message}")
        elif choice == '4':
            items = list_func(universe_repo, current_name)
            for i, item in enumerate(items):
                print(f"{i + 1}. {item}")
            item_choice = int(input(f"Choose a {lower_level}: ")) - 1
            update_current_location(state, current_universe, f"current_{lower_level}", items[item_choice])
        elif choice == '-':
            new_level = up_level
        elif choice == '+':
            new_level = down_level
        elif choice == '*':
            return  # Return to main menu
        elif choice == '0':
            return  # Return to main menu
        else:
            print("Invalid choice, please try again.")

        if new_level:
            if new_level != current_level: 
                state_data["current_level"] = new_level
                state_data["levels"][current_universe] = new_level
            new_level = None

if __name__ == "__main__":
    config_file = sys.argv[1] if len(sys.argv) > 1 else "DKT-WorldDataMan.conf"
    with open(config_file, 'r') as file:
        config_data = json.load(file)
    state_file = get_state_filename(config_file)
    state_data = load_state(state_file)
    print_state(state_data)
    universes = []
    for universe in config_data["universes"]:
        if t:= get_universe_details(universe['repo']):
            universes_details[universe["name"]] = t 
            universes.append(universe["name"])

    print_state(universes_details)
    print_state(universes)
    if "current_universe" in state_data and state_data["current_universe"] in universes:
        navigate_worldbuilding_space()
    main_menu(config_file)
