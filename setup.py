import os
from colorama import Fore, Style

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

{Fore.RESET}
{Fore.YELLOW}REQUIREMENTS INSTALLER v1.0 -- BY XABIT{Fore.RESET}
'''
    print(banner)

def install_requirements():
    print(Fore.YELLOW + "Installing required packages manually..." + Fore.RESET)

    # Manually installing each package
    os.system('pip3 install requests')
    os.system('pip3 install colorama')
    os.system('pip3 install pyfiglet')

if __name__ == "__main__":
    print_banner()
    install_requirements()
    print(Fore.GREEN + "All requirements have been successfully installed!" + Style.RESET_ALL)
