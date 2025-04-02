import os
import binascii
import json
import qrcode
import asyncio
from mnemonic import Mnemonic
from bip32utils import BIP32Key, BIP32_HARDEN
from service.balance import AsyncBlockstreamBalanceChecker
import hashlib
import base58
from eth_account import Account
from eth_utils import keccak
from eth_account.hdaccount import ETHEREUM_DEFAULT_PATH
import random

proxies = []

def set_proxies():
    list_proxies = open('proxy.txt').readlines()
    return list_proxies
proxies = set_proxies()

# 1. Генерация энтропии
class EntropyGenerator:
    def generate(self, bits: int = 128) -> str:
        entropy = os.urandom(bits // 8)
        return binascii.hexlify(entropy).decode()

# 2. Генерация и проверка мнемоники
class MnemonicGenerator:
    def __init__(self, language='english'):
        self.mnemo = Mnemonic(language)

    def generate_from_entropy(self, entropy: str) -> str:
        return self.mnemo.to_mnemonic(bytes.fromhex(entropy))

    def validate(self, phrase: str) -> bool:
        return self.mnemo.check(phrase)

# 3. Генерация сид-фразы
class SeedDeriver:
    def derive_seed(self, mnemonic: str, passphrase: str = "") -> str:
        return Mnemonic.to_seed(mnemonic, passphrase).hex()

# 4. HD Wallet и деривация по пути

class HDWallet:
    def __init__(self, seed_hex: str):
        seed = bytes.fromhex(seed_hex)
        self.master_key = BIP32Key.fromEntropy(seed)

    def derive_path(self, path: str) -> BIP32Key:
        node = self.master_key
        for part in path.strip('m/').split('/'):
            hardened = part.endswith("'")
            index = int(part.rstrip("'"))
            node = node.ChildKey(index + BIP32_HARDEN if hardened else index)
        return node

    def get_eth_address(self, derived_key: BIP32Key) -> str:
        pub_key = derived_key.PublicKey()[1:]  # remove 0x04 prefix
        address_bytes = keccak(pub_key)[-20:]  # keccak256 + take last 20 bytes
        return '0x' + address_bytes.hex()

    def get_ltc_address(self, derived_key: BIP32Key) -> str:
        pub_key = derived_key.PublicKey()
        sha256 = hashlib.sha256(pub_key).digest()
        ripemd160 = hashlib.new('ripemd160', sha256).digest()
        prefixed = b'\x30' + ripemd160  # 0x30 for LTC mainnet P2PKH
        checksum = hashlib.sha256(hashlib.sha256(prefixed).digest()).digest()[:4]
        return base58.b58encode(prefixed + checksum).decode()
    
    def get_doge_address(self, derived_key: BIP32Key) -> str:
        pub_key = derived_key.PublicKey()
        sha256 = hashlib.sha256(pub_key).digest()
        ripemd160 = hashlib.new('ripemd160', sha256).digest()
        prefixed = b'\x1e' + ripemd160  # 0x1e для DOGE mainnet
        checksum = hashlib.sha256(hashlib.sha256(prefixed).digest()).digest()[:4]
        return base58.b58encode(prefixed + checksum).decode()

    def get_bch_address(self, derived_key: BIP32Key) -> str:
        pub_key = derived_key.PublicKey()
        sha256 = hashlib.sha256(pub_key).digest()
        ripemd160 = hashlib.new('ripemd160', sha256).digest()
        prefixed = b'\x00' + ripemd160  # 0x00 как у BTC (Blockchair понимает)
        checksum = hashlib.sha256(hashlib.sha256(prefixed).digest()).digest()[:4]
        return base58.b58encode(prefixed + checksum).decode()



# 5. Генерация QR-кода
class QRCodeGenerator:
    def generate(self, data: str, output_file: str):
        img = qrcode.make(data)
        img.save(output_file)

# 6. Экспорт/импорт JSON
class WalletExporter:
    def export_to_json(self, data: dict, filepath: str):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def import_from_json(self, filepath: str) -> dict:
        with open(filepath, 'r') as f:
            return json.load(f)

# 7. Основной класс приложения
class BIP39WalletApp:
    def __init__(self):
        self.entropy_generator = EntropyGenerator()
        self.mnemonic_generator = MnemonicGenerator()
        self.seed_deriver = SeedDeriver()
        self.qr_generator = QRCodeGenerator()
        self.exporter = WalletExporter()
        self.balance_checker = AsyncBlockstreamBalanceChecker(proxy=random.choice(proxies))

    def create_wallet_data(self, coin: str = "BTC", passphrase: str = "") -> dict:
        path_map = {
            "BTC": "m/44'/0'/0'/0/0",
            "ETH": "m/44'/60'/0'/0/0",
            "LTC": "m/44'/2'/0'/0/0",
            "DOGE": "m/44'/3'/0'/0/0",
            "BCH":  "m/44'/145'/0'/0/0",
            "USDT": "m/44'/60'/0'/0/0",
        }

        if coin not in path_map:
            raise ValueError(f"Unsupported coin: {coin}")

        path = path_map[coin]
        entropy = self.entropy_generator.generate()
        mnemonic = self.mnemonic_generator.generate_from_entropy(entropy)
        seed = self.seed_deriver.derive_seed(mnemonic, passphrase)
        wallet = HDWallet(seed)
        derived_key = wallet.derive_path(path)

        if coin == "BTC":
            address = derived_key.Address()
        elif coin == "ETH":
            address = wallet.get_eth_address(derived_key)
        elif coin == "LTC":
            address = wallet.get_ltc_address(derived_key)
        elif coin == "DOGE":
            address = wallet.get_doge_address(derived_key)
        elif coin == "BCH":
            address = wallet.get_bch_address(derived_key)

        return {
            "coin": coin,
            "entropy": entropy,
            "mnemonic": mnemonic,
            "seed": seed,
            "path": path,
            "address": address,
            "public_key": derived_key.PublicKey().hex(),
            "private_key": derived_key.WalletImportFormat() if coin != "ETH" else derived_key.PrivateKey().hex()
        }


    def generate_qr_code(self, address: str, output_file: str):
        self.qr_generator.generate(address, output_file)

    def export_wallet(self, data: dict, filepath: str):
        self.exporter.export_to_json(data, filepath)

    async def check_balance(self, address: str) -> int:
        return await self.balance_checker.get_balance(address)



async def main():
    app = BIP39WalletApp()

    for coin in ["BTC", "ETH", "LTC"]:
        wallet_data = app.create_wallet_data(coin=coin)
        print(f"\n=== {coin} Wallet ===")
        print(json.dumps(wallet_data, indent=4))

        filename = f'{coin.lower()}_qr.png'
        app.generate_qr_code(wallet_data['address'], filename)
        app.export_wallet(wallet_data, f'{coin.lower()}_wallet.json')

        if coin == "BTC":
            balance = await app.check_balance(wallet_data['address'])
            print(f"Баланс BTC: {balance / 1e8:.8f} BTC")

if __name__ == "__main__":
    asyncio.run(main())
