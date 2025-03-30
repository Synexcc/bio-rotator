import requests
import json
import time
import datetime
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Constants for colors
RESET = Fore.RESET
MAGENTA = Fore.MAGENTA
BLACK = Fore.LIGHTBLACK_EX
GREEN = Fore.GREEN
RED = Fore.RED
CYAN = Fore.CYAN
YELLOW = Fore.YELLOW

# Load configuration
def load_config():
    try:
        with open("config.json", "r") as file:
            print(f"{BLACK}{get_current_time()} -> {MAGENTA}[Info] Loading Config...{RESET}")
            config = json.load(file)
            print(f"{BLACK}{get_current_time()} -> {GREEN}[Success] Done Loading Config{RESET}")
            return config
    except FileNotFoundError:
        print(f"{BLACK}{get_current_time()} -> {RED}[Error] Config file not found.{RESET}")
        exit(1)
    except json.JSONDecodeError:
        print(f"{BLACK}{get_current_time()} -> {RED}[Error] Invalid JSON in config file.{RESET}")
        exit(1)

# Get current time in HH:MM:SS format
def get_current_time():
    return datetime.datetime.now().strftime('%H:%M:%S')

# Update Discord profile
def update_profile(bio=None, pronouns=None):
    url = "https://discord.com/api/v9/users/@me/profile"
    payload = {}
    if bio:
        payload["bio"] = bio
    if pronouns:
        payload["pronouns"] = pronouns

    headers = {
        "Authorization": config["Token"],
        "Content-Type": "application/json"
    }

    try:
        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code == 200:
            if bio and pronouns:
                print(f"{BLACK}{get_current_time()} -> {GREEN}[Success] Updated Bio to '{CYAN}{bio}{GREEN}' and Pronouns to '{CYAN}{pronouns}{GREEN}'{RESET}")
            elif bio:
                print(f"{BLACK}{get_current_time()} -> {GREEN}[Success] Updated Bio to '{CYAN}{bio}{GREEN}'{RESET}")
            elif pronouns:
                print(f"{BLACK}{get_current_time()} -> {GREEN}[Success] Updated Pronouns to '{CYAN}{pronouns}{GREEN}'{RESET}")
        else:
            print(f"{BLACK}{get_current_time()} -> {RED}[Failed] HTTP Error {response.status_code}: {response.text}{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{BLACK}{get_current_time()} -> {RED}[Error] Connection failed: {e}{RESET}")

# Main function
def main():
    global config
    config = load_config()

    # Ask user for mode
    print(f"{BLACK}{get_current_time()} -> {MAGENTA}[?] Choose mode: {CYAN}bio{RESET}, {CYAN}pronouns{RESET}, or {CYAN}both{RESET}")
    mode = input(f"{BLACK}{get_current_time()} -> {MAGENTA}[?] {RESET}").strip().lower()

    if mode not in ["bio", "pronouns", "both"]:
        print(f"{BLACK}{get_current_time()} -> {RED}[Error] Invalid mode. Use 'bio', 'pronouns', or 'both'.{RESET}")
        time.sleep(2)
        exit(1)

    # Main loop
    while True:
        if mode == "bio":
            update_profile(bio=config["Bio_1"])
            time.sleep(config["Delay"])
            update_profile(bio=config["Bio_2"])
            time.sleep(config["Delay"])
        elif mode == "pronouns":
            update_profile(pronouns=config["Pronoun_1"])
            time.sleep(config["Delay"])
            update_profile(pronouns=config["Pronoun_2"])
            time.sleep(config["Delay"])
        elif mode == "both":
            update_profile(bio=config["Bio_1"], pronouns=config["Pronoun_1"])
            time.sleep(config["Delay"])
            update_profile(bio=config["Bio_2"], pronouns=config["Pronoun_2"])
            time.sleep(config["Delay"])

if __name__ == "__main__":
    print(f"{BLACK}{get_current_time()} -> {CYAN}Starting Discord Profile Updater...{RESET}")
    main()