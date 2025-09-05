import os
import time
from colorama import init, Fore, Style
from api import SupremeModz

init(autoreset=True)

VERSION = "1.0.0"
DEV_LINK = "https://t.me/Suprememodz"

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def header():
    print(Fore.CYAN + "=" * 59)
    print(Fore.WHITE + f"• Car Parking Multiplayer 2 - Version: {VERSION} || Dev: {DEV_LINK}")
    print(Fore.CYAN + "=" * 59)

def print_title_inside_line(title, width=59):
    title_str = f"[ {title} ]"
    total_len = width
    side_len = max(0, (total_len - len(title_str) - 2) // 2)

    left = Fore.CYAN + ("=" * side_len) + " "

    center = Fore.CYAN + "[" + Fore.WHITE + f" {title} " + Fore.CYAN + "]"

    base_len = side_len + 1 + len(title_str) + 1 + side_len
    extra = max(0, total_len - base_len)
    right = " " + Fore.CYAN + ("=" * (side_len + extra))

    print(left + center + right + Style.RESET_ALL)

def print_info(label, value, color=Fore.WHITE):
    print(color + f"{label:<12} : {value}")

def executar_servico(func, token, chave, email, password, pedir_valor=False):
    """Runs a service by calling the utils function and shows result on the same line"""
    amount = None
    if pedir_valor:
        try:
            amount = int(input(Fore.YELLOW + "• Enter New Value: " + Style.RESET_ALL).strip())
        except ValueError:
            print(Fore.RED + "• Running Service: Invalid value.")
            time.sleep(2)
            return None

    print(Fore.WHITE + "• Running Service: " + Style.RESET_ALL, end="")

    try:
        if pedir_valor:
            resp = func(chave=chave, token=token, amount=amount, api_url=API_URL)
        else:
            resp = func(chave=chave, token=token, api_url=API_URL)

        if resp.get("status_code") == 200 or resp.get("status") == "ok":
            print(Fore.LIGHTGREEN_EX + "Success")
        else:
            msg = resp.get("message") or str(resp)
            print(Fore.RED + f"Error: {msg}")

    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}")
        return None

    while True:
        opt = input(Fore.WHITE + "• Return To Main Menu? (Y/N): " + Style.RESET_ALL).strip().lower()
        if opt == "y":
            return True
        elif opt == "n":
            print(Fore.CYAN + "Bye Bye...")
            exit(0)
        else:
            print(Fore.RED + "❌ Invalid option! Type only Y or N.")
            time.sleep(2)

def menu_loop(dados, token, chave, email, password):
    while True:
        clear()
        header()

        print_title_inside_line("User Detail")
        print_info("ID", dados.get("id"))
        print_info("Key", dados.get("key"))
        print_info("Valid Until", dados.get("valid_until"))

        print_title_inside_line("Player Information")
        print_info("Name", dados.get("name"))
        print_info("LocalId", dados.get("localid"))
        print_info("Money", dados.get("money"))
        print_info("Coins", dados.get("coins"))
        print_info("Slots", dados.get("slots"))
        print_info("Cars", dados.get("cars_count"))

        print_title_inside_line("Menu")
        print(Fore.WHITE + "[" + Fore.CYAN + "01" + Fore.WHITE + "] Inject Account In Generator.")
        print(Fore.WHITE + "[" + Fore.CYAN + "02" + Fore.WHITE + "] Unlock Redrock garage .")
        print(Fore.WHITE + "[" + Fore.CYAN + "00" + Fore.WHITE + "] Exit Tool.")

        print(Fore.CYAN + "=" * 59)
        opt = input(
            Fore.WHITE + "Input Menu Number " +
            Fore.CYAN + "[" + 
            Fore.WHITE + "00 - 02" + 
            Fore.CYAN + "]" + 
            Style.RESET_ALL + ": "
        ).strip()

        if opt in ("0", "00"):
            print(Fore.CYAN + "Bye Bye...")
            return False
        elif opt in ("1", "01"):
            return executar_servico(inject_account, token, chave, email, password)
        else:
            print(Fore.RED + "Invalid Option. Reloading Menu In 3 Seconds...")
            time.sleep(3)

def login_e_menu(key, email, password):
    """Login and Main Menu"""
    key_result = verificar_key_com_fingerprint(key, api_url=API_URL)
    if key_result.get("status") != "ok":
        print(Fore.RED + key_result.get("message", "Unknown error.") + Style.RESET_ALL)
        time.sleep(3)
        return False

    token = key_result.get("token")
    if not token:
        print(Fore.RED + "❌ Token not returned." + Style.RESET_ALL)
        time.sleep(3)
        return False

    login_result = login(chave=key, email=email, password=password, token=token, api_url=API_URL)
    if not login_result.get("success"):
        print(Fore.RED + login_result.get("message", "Unknown login error.") + Style.RESET_ALL)
        time.sleep(3)
        return False

    dados_para_menu = {
        "id": key_result.get("id"),
        "key": key,
        "valid_until": key_result.get("valid_until"),
        "name": login_result.get("name"),
        "localid": login_result.get("localid"),
        "money": login_result.get("money"),
        "coins": login_result.get("coins"),
        "slots": login_result.get("slots"),
        "cars_count": login_result.get("cars_count")
    }

    return menu_loop(dados_para_menu, token, key, email, password)

def main():
    try:
        clear()
        header()

        key = input(Fore.WHITE + "• Enter Your Key: " + Style.RESET_ALL).strip()
        if not key:
            print(Fore.RED + "Empty key.")
            time.sleep(3)
            return

        email = input(Fore.WHITE + "• Enter Your Email: " + Style.RESET_ALL).strip()
        if not email:
            print(Fore.RED + "Empty email.")
            time.sleep(3)
            return

        password = input(Fore.WHITE + "• Enter Your Password: " + Style.RESET_ALL).strip()
        if not password:
            print(Fore.RED + "Empty password.")
            time.sleep(3)
            return

        print(Fore.WHITE + "• Verifying Key: " + Style.RESET_ALL, end="")
        key_result = SupremeModz(key, api_url="https://admincpm.io/KrishPV/api")
        if key_result.get("status") != "ok":
            print(Fore.RED + key_result.get("message", "Unknown error.") + Style.RESET_ALL)
            time.sleep(3)
            return
        print(Fore.LIGHTGREEN_EX + "Success")

        token = key_result.get("token")
        if not token:
            print(Fore.RED + "❌ Token not returned.")
            time.sleep(3)
            return

        print(Fore.WHITE + "• Logging In: " + Style.RESET_ALL, end="")
        login_result = login(chave=key, email=email, password=password, token=token, api_url=API_URL)
        if not login_result.get("success"):
            print(Fore.RED + login_result.get("message", "Unknown login error.") + Style.RESET_ALL)
            time.sleep(3)
            return
        print(Fore.LIGHTGREEN_EX + "Success")

        time.sleep(3)

        dados_para_menu = {
            "id": key_result.get("id"),
            "key": key,
            "valid_until": key_result.get("valid_until"),
            "name": login_result.get("name"),
            "localid": login_result.get("localid"),
            "money": login_result.get("money"),
            "coins": login_result.get("coins"),
            "slots": login_result.get("slots"),
            "cars_count": login_result.get("cars_count")
        }

        reload_menu = menu_loop(dados_para_menu, token, key, email, password)

        while reload_menu:
            reload_menu = login_e_menu(key, email, password)
            if not reload_menu:
                break

    except KeyboardInterrupt:
        print("\n" + Fore.CYAN + "Bye Bye...")

if __name__ == "__main__":
    main()