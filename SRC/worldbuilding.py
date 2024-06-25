import os
import json
import subprocess

uncommitted_changes = {}

def init_hier(path, author, type_name, additional_paths=[], commit_message=None):
    if not os.path.exists(path):
        os.makedirs(path)
    
    settings_file = os.path.join(path, "settings.json")
    common_paths = ["components", "arcs", "timelines"]
    all_paths = common_paths + additional_paths

    if not os.path.exists(settings_file):
        data = {
            "layout_version": "0.1.0",
            "name": os.path.basename(path),
            "tooltip": f"A brief description of the {type_name}",
            "primary_authors": [author],
            "secondary_authors": [],
            "contributing_authors": []
        }
        with open(settings_file, 'w') as file:
            json.dump(data, file, indent=4)
    
    for sub_path in all_paths:
        full_path = os.path.join(path, sub_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

    if commit_message is not None:
        repo_path = os.path.dirname(os.path.dirname(path))
        if repo_path not in uncommitted_changes:
            uncommitted_changes[repo_path] = ""
        uncommitted_changes[repo_path] += f"{commit_message}\n"

def init_galaxy(repo_path, galaxy_name, author, commit_message=None):
    galaxy_path = os.path.join(repo_path, "galaxies", galaxy_name)
    init_hier(galaxy_path, author, "galaxy", ["worlds"], commit_message)

def init_world(repo_path, galaxy_name, world_name, author, commit_message=None):
    world_path = os.path.join(repo_path, "galaxies", galaxy_name, "worlds", world_name)
    init_hier(world_path, author, "world", ["stories"], commit_message)

def init_story(repo_path, galaxy_name, world_name, story_name, author, commit_message=None):
    story_path = os.path.join(repo_path, "galaxies", galaxy_name, "worlds", world_name, "stories", story_name)
    init_hier(story_path, author, "story", [], commit_message)

def init_universe(repo_path, author, commit_message=None):
    init_hier(repo_path, author, "universe", ["galaxies"], commit_message)

def add_universe(config_file, universe_repo, author):
    config_data = load_config(config_file)
    init_universe(universe_repo, author, f"Add universe {os.path.basename(universe_repo)}")
    config_data["universes"].append({
        "name": os.path.basename(universe_repo),
        "repo": universe_repo
    })
    save_config(config_file, config_data)

def list_galaxies(repo_path):
    galaxies_path = os.path.join(repo_path, "galaxies")
    if os.path.exists(galaxies_path):
        return [galaxy for galaxy in os.listdir(galaxies_path) if os.path.isdir(os.path.join(galaxies_path, galaxy))]
    else:
        return []

def list_worlds(repo_path, galaxy_name):
    worlds_path = os.path.join(repo_path, "galaxies", galaxy_name, "worlds")
    if os.path.exists(worlds_path):
        return [world for world in os.listdir(worlds_path) if os.path.isdir(os.path.join(worlds_path, world))]
    else:
        return []

def list_stories(repo_path, galaxy_name, world_name):
    stories_path = os.path.join(repo_path, "galaxies", galaxy_name, "worlds", world_name, "stories")
    if os.path.exists(stories_path):
        return [story for story in os.listdir(stories_path) if os.path.isdir(os.path.join(stories_path, story))]
    else:
        return []

def commit_changes(repo_path):
    if repo_path in uncommitted_changes and uncommitted_changes[repo_path]:
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", uncommitted_changes[repo_path].strip()], cwd=repo_path, check=True)
        uncommitted_changes[repo_path] = ""
        print(f"Changes committed to {repo_path}")
    else:
        print("No changes to commit.")

def get_universe_details(repo_path):
    name = os.path.basename(repo_path)
    tooltip = "No description available"
    git_status = "No Git repository"
    git_version = "Unknown"

    settings_file = os.path.join(repo_path, "settings.json")
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as file:
            settings = json.load(file)
            name = settings.get("name", name)
            tooltip = settings.get("tooltip", tooltip)

    if os.path.exists(os.path.join(repo_path, ".git")):
        git_status = subprocess.run(["git", "status", "--short"], cwd=repo_path, capture_output=True, text=True).stdout.strip()
        git_version = subprocess.run(["git", "log", "-1", "--format=%ad"], cwd=repo_path, capture_output=True, text=True).stdout.strip()

        return {
        "name": name,
        "tooltip": tooltip,
        "git_status": git_status,
        "git_version": git_version
    }
