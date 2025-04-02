import asyncio
import argparse
import json
from service.indb_mode import run_indb_generate, run_indb_ping
import random
from pathlib import Path
from datetime import datetime
from colorama import Fore
from service.mnemonic_service import BIP39WalletApp
from service.balance import AsyncBlockstreamBalanceChecker,AsyncBscScanBalanceChecker,AsyncBlockchairBCHChecker,AsyncEtherscanUSDTChecker,AsyncEtherscanBalanceChecker,AsyncDogecoinMultiChecker,AsyncLitecoinMultiChecker,MultiAddressBalanceManager
from service.only_generate import run_only_generate_txt
import time
from gui.entity.logo import Logo
from gui.symbols.ascii import GUISymbols
from gui.messages.default import title, change, action, error, debug_row, success
from gui.entity.menu import Menu
from gui.messages.framed import FramedMessage
from utils.system_utils import clear_console
clear_console()

proxies = []
symbols = GUISymbols()

def set_proxies():
    list_proxies = open('proxy.txt').readlines()
    return list_proxies

def display_proxies():
    menu = Menu("Установленые проки")
    for proxy in proxies:
        menu.add_item(proxy)
    menu.display()


proxies = set_proxies()
if proxies:
    
    display_proxies()
    time.sleep(2)

# GUI запуск
def run_gui_menu():
    logo = Logo(name='Nollieundergrob', description='BIP39 Wallet manager')
    symbols = GUISymbols()
    logo.display_logo()
    logo.display()

    title("Добро пожаловать в Wallet Generator")
    change("Вы можете создать BIP39 кошельки, проверить их баланс и сохранить результат.")

    menu = Menu(title='Выберите режим:')
    menu.add_item("Запуск с настройками по умолчанию")
    menu.add_item("Указать количество кошельков")
    menu.add_item("Указать название файла для сохранения")
    menu.add_item("Включить подробные логи")
    menu.add_item("Бесконечный режим генерации")
    menu.add_item("InDB: Генерация и сохранение в БД")
    menu.add_item("InDB: Пинг API для адресов")
    menu.add_item("Сгенерировать только один параметр (private_key/mnemonic/address)")

    menu.display()
    return menu.get_choice()

# Основной запуск
async def main():
    parser = argparse.ArgumentParser(description="BIP39 Wallet Generator")
    parser.add_argument("-t", "--threads", type=int, help="Количество кошельков для генерации")
    parser.add_argument("-v", "--verbose", action="store_true", help="Вывод логов каждой операции")
    parser.add_argument("-f", "--file", type=str, help="Название файла для сохранения результатов в папку ./export")
    parser.add_argument("--infinite", action="store_true", help="Запустить бесконечный режим")
    args = parser.parse_args()

    threads = args.threads if args.threads else 10
    verbose = args.verbose
    filename = args.file
    infinite = args.infinite

    if not any([args.threads, args.verbose, args.file, args.infinite]):
        choice = run_gui_menu()
        print(choice)
        if choice == 'Указать количество кошельков':
            threads = int(input("Введите количество кошельков: "))
        elif choice == 'Указать название файла для сохранения':
            filename = input("Введите название файла: ")
        elif choice == 'Включить подробные логи':
            verbose = True
        elif choice == 'Бесконечный режим генерации':
            infinite = True
        elif choice == 'InDB: Генерация и сохранение в БД':
            count= int(input('Введите кол-во адресов ->'))
            await run_indb_generate(count=count)
            return 0
        elif choice =='Сгенерировать только один параметр (private_key/mnemonic/address)':
            framed = FramedMessage(padding=5,border_color=Fore.GREEN)
            print(framed.create_frame('Введите кол-во адресов'))
            count= int(input('-> '))
            print(framed.create_frame('Введите название монеты (BTC/ETH/USDT/LTC/DOGE/BCH):'))
            coin_menu = Menu("Выберите монету")
            coin_menu.add_item('BTC')
            coin_menu.add_item('ETH')
            coin_menu.add_item('USDT')
            coin_menu.add_item("LTC")
            coin_menu.add_item("DOGE")
            coin_menu.add_item("BCH")
            coin_menu.display()
            coin_menu=coin_menu.get_choice()
            
            print(framed.create_frame('Введите название файла:'))
            filename = input("-> ")
            type_menu = Menu("Выберите тип данных")
            type_menu.add_item('private_key')
            type_menu.add_item('mnemonic')
            type_menu.add_item('address')
            type_menu.display()
            type_menu = type_menu.get_choice()
            await run_only_generate_txt(count=count, coin=coin_menu, out_file=filename,data_type = type_menu)
            return 0
        elif choice == 'InDB: Пинг API для адресов':
            if proxies:
                await run_indb_ping(proxy=random.choice(proxies))
            else:
                await run_indb_ping()
            return 0


    print(choice,choice=="Бесконечный режим генерации",infinite)
    app = BIP39WalletApp()
    framed = FramedMessage(padding=5)
    framed.create_frame('Генерирую кошельки')

    async def generate_and_store(index: int, path: Path):
        data = app.create_wallet_data()
        balance_sats = await app.check_balance(data['address'])
        balance_btc = f"{balance_sats / 1e8:.8f} BTC"

        result = {
                    "address": data['address'],
                    "private_key": data['private_key'],
                    "public_key": data['public_key'],
                    "balance": balance_btc,
                    "mnemonic":data['mnemonic'],
                    "seed":data['seed'],
                }

        msg = f"Кошелёк #{index} — " + ";\n".join([f"{k}: {v}" for k, v in result.items()])
        if balance_sats > 0:
            success(msg)
        else:
            print(framed.create_frame(msg))

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'a') as f:
            json.dump({str(index): result}, f, ensure_ascii=False)
            f.write(",\n")
            
    if infinite:
        coins = ["BTC","ETH"]
        eth_checker = AsyncEtherscanBalanceChecker(api_key="WSYDP386X5EIT3HXAXTAZSXHR8GCD943DA",proxy=random.choice(proxies))
        checkers = [
            AsyncBlockstreamBalanceChecker(proxy=random.choice(proxies)),
            AsyncLitecoinMultiChecker(proxy=random.choice(proxies)),
            AsyncBscScanBalanceChecker(api_key="YOUR_BSCSCAN_API_KEY",proxy=random.choice(proxies)),
           # AsyncBlockchairBCHChecker(proxy=random.choice(proxies)),
            AsyncDogecoinMultiChecker(proxy=random.choice(proxies)),
            eth_checker,
        ]
        balance_manager = MultiAddressBalanceManager(checkers)

        path = Path("export") / f"infinite_multi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        index = 1

    async def generate_and_store_multi(index: int, path: Path):
        wallets_by_currency = {}
        all_wallet_data = {}

        # Генерируем по одному адресу на каждую валюту
        for coin in coins:
            try:
                data = app.create_wallet_data(coin=coin)
                address = data['address']
                wallets_by_currency.setdefault(coin, []).append(address)
                all_wallet_data[coin] = {
                    "address": address,
                    "private_key": data['private_key'],
                    "public_key": data['public_key'],
                    "mnemonic": data['mnemonic'],
                    "seed": data['seed'],
                    "path": data['path']
                }
            except Exception as e:
                print(f"Ошибка генерации {coin}: {e}")

        balances = await balance_manager.get_all_balances(wallets_by_currency)

        result = {}
        for coin, addr_data in balances.items():
            for addr, balance in addr_data.items():
                all_wallet_data[coin]["balance"] = (
                    f"{balance / 1e8:.8f}" if coin in ["BTC", "LTC", "DOGE", "BCH"] else str(balance)
                )
                result[coin] = all_wallet_data[coin]

        msg = f"\n=== Wallet Set #{index} ===\n"
        for coin, data in result.items():
            msg += f"[{coin}] {data['address']} — Balance: {data.get('balance')}\n"

        print(framed.create_frame(msg.strip()))

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'a', encoding="utf-8") as f:
            json.dump({str(index): result}, f, ensure_ascii=False)
            f.write(",\n")
    if infinite:
        while True:
            await generate_and_store_multi(index, path)
            index += 1
            await asyncio.sleep(1)

    else:
        result = {}
        semaphore = asyncio.Semaphore(3)

        async def process_wallet(index: int):
            async with semaphore:
                data = app.create_wallet_data()
                balance_sats = await app.check_balance(data['address'])
                balance_btc = f"{balance_sats / 1e8:.8f} BTC"

                result[str(index)] = {
                    "address": data['address'],
                    "private_key": data['private_key'],
                    "public_key": data['public_key'],
                    "balance": balance_btc,
                    "mnemonic":data['mnemonic'],
                    "seed":data['seed'],
                }

                msg = f"Кошелёк #{index} — " + ", ".join([f"{k}: {v}" for k, v in result[str(index)].items()])
                if balance_sats > 0:
                    success(msg)
                else:
                    action(msg)

        await asyncio.gather(*(process_wallet(i) for i in range(1, threads + 1)))

        if filename:
            export_path = Path("export") / f"{filename}.json"
            app.export_wallet(result, str(export_path))
            change(f"Результат сохранён в файл: {export_path}")

if __name__ == "__main__":
    asyncio.run(main())
