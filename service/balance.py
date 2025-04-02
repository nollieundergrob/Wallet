import httpx
from abc import ABC, abstractmethod
from gui.exceptions.ItrenalAppException import ItrenalAppException
from gui.messages.framed import FramedMessage
from colorama import Fore,Back,Style
from gui.messages import error
import datetime
import time
import asyncio
class AbstractBalanceChecker(ABC):
    
    @property
    @abstractmethod
    def currency(self) -> str:
        pass
    @abstractmethod
    async def get_balance(self, address: str) -> int:
        pass

class AsyncBlockstreamBalanceChecker(AbstractBalanceChecker):
    BASE_URL = "https://blockstream.info/api"
    sleep=0.01
    
    def __init__(self,proxy):
        self.proxy = proxy
        
    @property
    def currency(self):
        return 'BTC'

    async def get_balance(self, address: str) -> int:
        url = f"{self.BASE_URL}/address/{address}"
        time.sleep(self.sleep)
        if self.proxy:
            async with httpx.AsyncClient(proxy=self.proxy) as client:
                response = await client.get(url)
        else:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

        if response.status_code == 429:
            self.sleep += 30 * self.sleep / 100
            framed = FramedMessage(padding=5)
            print(framed.create_frame(f"Немного увеличим задерку, попробуем снова... {self.sleep} секунд"))
            return await self.get_balance(address)
        
        if response.status_code != 200:
            raise ItrenalAppException(
                "Ошибка получения баланса: {status_code}",
               {"code": {response.status_code}, "time": f"{datetime.datetime.now()}", "details": f"{''.join([f"{key}:{value}\n" for key,value in response.__dict__.items()])}"},
               status_code=response.status_code
                )
        if response.status_code == 200:
            self.sleep -= 60 * self.sleep / 100
        

        data = response.json()
        funded = data.get("chain_stats", {}).get("funded_txo_sum", 0)
        spent = data.get("chain_stats", {}).get("spent_txo_sum", 0)
        return funded - spent


class AsyncEtherscanBalanceChecker(AbstractBalanceChecker):
    BASE_URL = "https://api.etherscan.io/api"
    sleep = 0.01
    

    def __init__(self, api_key: str, proxy: str = None):
        self.api_key = api_key
        self.proxy=  proxy
        
    @property
    def currency(self) -> str:
        return "ETH"

    async def get_balance(self, address: str) -> int:
        params = {
            "module": "account",
            "action": "balance",
            "address": address,
            "tag": "latest",
            "apikey": self.api_key
        }

        time.sleep(self.sleep)
        if self.proxy:
            async with httpx.AsyncClient(proxy=self.proxy) as client:
                response = await client.get(self.BASE_URL,params=params)
        else:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.BASE_URL,params=params)

        if response.status_code == 429:
            self.sleep += 30 * self.sleep / 100
            framed = FramedMessage(padding=5)
            print(framed.create_frame(f"Немного увеличим задерку, попробуем снова... {self.sleep} секунд"))
            return await self.get_balance(address)
        
        if response.status_code != 200:
            raise ItrenalAppException(
                "Ошибка получения баланса: {status_code}",
               {"code": {response.status_code}, "time": f"{datetime.datetime.now()}", "details": f"{''.join([f"{key}:{value}\n" for key,value in response.__dict__.items()])}"},
               status_code=response.status_code
                )
        if response.status_code == 200:
            self.sleep -= 60 * self.sleep / 100
        result = response.json()

        wei_balance = int(result["result"])
        return wei_balance // 10**18


from gui.messages.default import warning, error, debug_row
from gui.messages.framed import FramedMessage
from gui.exceptions.ItrenalAppException import ItrenalAppException
import datetime
import httpx

class AsyncLitecoinMultiChecker(AbstractBalanceChecker):
    sleep = 0.01

    def __init__(self, proxy: str = None):
        self.proxy = proxy

    @property
    def currency(self) -> str:
        return "LTC"

    async def _request(self, url: str) -> httpx.Response:
        try:
            if self.proxy:
                transport = httpx.AsyncHTTPTransport(proxy=self.proxy)
                async with httpx.AsyncClient(transport=transport) as client:
                    return await client.get(url)
            else:
                async with httpx.AsyncClient() as client:
                    return await client.get(url)
        except Exception as e:
            raise ItrenalAppException("Ошибка выполнения HTTP-запроса", {
                "url": url,
                "exception": str(e),
                "time": str(datetime.datetime.now())
            })

    async def get_balance(self, address: str) -> int:
        sources = [
            self._from_sochain,
            self._from_blockcypher,
        ]

        for fetch in sources:
            try:
                return await fetch(address)
            except Exception as e:
                warning(f"[LTC] Источник `{fetch.__name__}` не сработал: {e}")
                continue

        raise ItrenalAppException(
            "Не удалось получить баланс LTC ни с одного источника",
            {
                "address": address,
                "time": str(datetime.datetime.now())
            },
            debug=True
        )

    async def _from_sochain(self, address: str) -> int:
        url = f"https://sochain.com/api/v2/get_address_balance/LTC/{address}"
        response = await self._request(url)

        if response.status_code in (429, 500, 502, 503):
            raise Exception(f"SoChain отказался: {response.status_code}")

        result = response.json()
        confirmed = float(result["data"]["confirmed_balance"])
        debug_row(f"[SoChain] LTC баланс {address}: {confirmed} LTC")
        return int(confirmed * 10**8)

    async def _from_blockcypher(self, address: str) -> int:
        url = f"https://api.blockcypher.com/v1/ltc/main/addrs/{address}/balance"
        response = await self._request(url)

        if response.status_code != 200:
            raise Exception(f"BlockCypher отказался: {response.status_code}")

        result = response.json()
        debug_row(f"[BlockCypher] LTC баланс {address}: {result['balance']} сатоши")
        return int(result["balance"])

    async def _from_chainso(self, address: str) -> int:
        url = f"https://chain.so/api/v2/get_address_balance/LTC/{address}"
        response = await self._request(url)

        if response.status_code != 200:
            raise Exception(f"Chain.so отказался: {response.status_code}")

        result = response.json()
        confirmed = float(result["data"]["confirmed_balance"])
        debug_row(f"[Chain.so] LTC баланс {address}: {confirmed} LTC")
        return int(confirmed * 10**8)


class AsyncDogecoinMultiChecker(AbstractBalanceChecker):
    sleep = 0.01

    def __init__(self, proxy: str = None):
        self.proxy = proxy

    @property
    def currency(self) -> str:
        return "DOGE"

    async def _request(self, url: str) -> httpx.Response:
        if self.proxy:
            async with httpx.AsyncClient(proxy=self.proxy) as client:
                return await client.get(url)
        else:
            async with httpx.AsyncClient() as client:
                return await client.get(url)

    async def get_balance(self, address: str) -> int:
        sources = [
            self._from_sochain,
            self._from_blockcypher,
            self._from_chainso
        ]

        for fetch in sources:
            try:
                return await fetch(address)
            except Exception as e:
                err = FramedMessage(padding=2,border_color=Fore.RED)
                
                print(err.create_frame((f"[DOGE] {fetch.__name__} не сработал: {e}")))
                continue

        raise ItrenalAppException(
            "Не удалось получить баланс DOGE ни с одного источника",
            {"address": address, "time": str(datetime.datetime.now())}
        )

    async def _from_sochain(self, address: str) -> int:
        url = f"https://sochain.com/api/v2/get_address_balance/DOGE/{address}"
        response = await self._request(url)

        if response.status_code == 429:
            self.sleep += 0.3 * self.sleep
            print(f"[DOGE:SoChain] 429 — увеличиваем задержку: {self.sleep}")
            return await self._from_sochain(address)

        if response.status_code != 200:
            raise Exception(f"SoChain error: {response.status_code} — {response.text}")

        result = response.json()
        confirmed = float(result["data"]["confirmed_balance"])
        return int(confirmed * 10**8)

    async def _from_blockcypher(self, address: str) -> int:
        url = f"https://api.blockcypher.com/v1/doge/main/addrs/{address}/balance"
        response = await self._request(url)

        if response.status_code != 200:
            raise Exception(f"BlockCypher error: {response.status_code} — {response.text}")

        result = response.json()
        return int(result["balance"])  # Сатоши

    async def _from_chainso(self, address: str) -> int:
        url = f"https://chain.so/api/v2/get_address_balance/DOGE/{address}"
        response = await self._request(url)

        if response.status_code != 200:
            raise Exception(f"Chain.so error: {response.status_code} — {response.text}")

        result = response.json()
        confirmed = float(result["data"]["confirmed_balance"])
        return int(confirmed * 10**8)


class AsyncBlockchairBCHChecker(AbstractBalanceChecker):
    BASE_URL = "https://api.blockchair.com/bitcoin-cash"
    sleep = 0.01

    @property
    def currency(self) -> str:
        return "BCH"
    def __init__(self,proxy):
        self.proxy = proxy

    async def get_balance(self, address: str) -> int:
        url = f"{self.BASE_URL}/dashboards/address/{address}"

        if self.proxy:
            async with httpx.AsyncClient(proxy=self.proxy) as client:
                response = await client.get(url)
        else:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

        if response.status_code == 429:
            self.sleep += 30 * self.sleep / 100
            framed = FramedMessage(padding=5)
            print(framed.create_frame(f"Немного увеличим задерку, попробуем снова... {self.sleep} секунд"))
            return await self.get_balance(address)
        
        if response.status_code != 200:
            raise ItrenalAppException(
                "Ошибка получения баланса: {status_code}",
               {"code": {response.status_code}, "time": f"{datetime.datetime.now()}", "details": f"{''.join([f"{key}:{value}\n" for key,value in response.__dict__.items()])}"},
               status_code=response.status_code
                )
        if response.status_code == 200:
            self.sleep -= 60 * self.sleep / 100

        data = response.json()
        balance = data["data"][address]["address"]["balance"]
        return balance  


class AsyncBscScanBalanceChecker(AbstractBalanceChecker):
    BASE_URL = "https://api.bscscan.com/api"
    sleep = 0.01

    def __init__(self, api_key: str,proxy: str):
        self.api_key = api_key
        self.proxy = proxy

    @property
    def currency(self) -> str:
        return "BNB"

    async def get_balance(self, address: str) -> int:
        params = {
            "module": "account",
            "action": "balance",
            "address": address,
            "apikey": self.api_key
        }

        if self.proxy:
            async with httpx.AsyncClient(proxy=self.proxy) as client:
                response = await client.get(self.BASE_URL,params=params)
        else:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.BASE_URL,params=params)

        if response.status_code == 429:
            self.sleep += 30 * self.sleep / 100
            framed = FramedMessage(padding=5)
            print(framed.create_frame(f"Немного увеличим задерку, попробуем снова... {self.sleep} секунд"))
            return await self.get_balance(address)
        
        if response.status_code != 200:
            raise ItrenalAppException(
                "Ошибка получения баланса: {status_code}",
               {"code": {response.status_code}, "time": f"{datetime.datetime.now()}", "details": f"{''.join([f"{key}:{value}\n" for key,value in response.__dict__.items()])}"},
               status_code=response.status_code
                )
        if response.status_code == 200:
            self.sleep -= 60 * self.sleep / 100

        result = response.json()
        if result.get("status") != "1":
            raise ItrenalAppException(f"BscScan response error: {result.get('message')}")

        wei_balance = int(result["result"])
        return wei_balance // 10**18 

class AsyncEtherscanUSDTChecker(AbstractBalanceChecker):
    BASE_URL = "https://api.etherscan.io/api"
    USDT_CONTRACT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    sleep = 0.01

    def __init__(self, api_key: str,proxy:str=None):
        self.api_key = api_key
        self.proxy = proxy

    @property
    def currency(self) -> str:
        return "USDT"


    async def get_balance(self, address: str) -> int:
        params = {
            "module": "account",
            "action": "tokenbalance",
            "contractaddress": self.USDT_CONTRACT,
            "address": address,
            "tag": "latest",
            "apikey": self.api_key
        }

        if self.proxy:
            async with httpx.AsyncClient(proxy=self.proxy) as client:
                response = await client.get(self.BASE_URL,params=params)
        else:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.BASE_URL,params=params)

        if response.status_code == 429:
            self.sleep += 30 * self.sleep / 100
            framed = FramedMessage(padding=5)
            print(framed.create_frame(f"Немного увеличим задерку, попробуем снова... {self.sleep} секунд"))
            return await self.get_balance(address)
        
        if response.status_code != 200:
            raise ItrenalAppException(
                "Ошибка получения баланса: {status_code}",
               {"code": {response.status_code}, "time": f"{datetime.datetime.now()}", "details": f"{''.join([f"{key}:{value}\n" for key,value in response.__dict__.items()])}"},
               status_code=response.status_code
                )
        if response.status_code == 200:
            self.sleep -= 60 * self.sleep / 100

        result = response.json()
        if result.get("status") != "1":
            raise ItrenalAppException("Ошибка в ответе Etherscan USDT {result}",{result},result=result)

        raw_balance = int(result["result"])
        return raw_balance // 10**6
    
    
    
    
    
class MultiAddressBalanceManager:
    def __init__(self, checkers: list[AbstractBalanceChecker]):
        self.checkers_map = {checker.currency: checker for checker in checkers}

    async def get_all_balances(self, wallets: dict[str, list[str]]) -> dict[str, dict[str, int]]:
        """
        wallets: {
            "BTC": ["addr1", "addr2"],
            "ETH": ["addr3"]
        }

        Returns:
        {
            "BTC": {"addr1": 1234, "addr2": 5678},
            "ETH": {"addr3": 9999}
        }
        """
        tasks = []
        for currency, addresses in wallets.items():
            checker = self.checkers_map.get(currency)
            if not checker:
                print(f"[!] Нет чекера для валюты: {currency}")
                continue

            for addr in addresses:
                tasks.append(self._get_balance_safe(checker, addr))

        results = await asyncio.gather(*tasks)

        balances_by_currency = {}
        for currency, address, balance in results:
            balances_by_currency.setdefault(currency, {})[address] = balance

        return balances_by_currency

    async def _get_balance_safe(self, checker: AbstractBalanceChecker, address: str) -> tuple[str, str, int]:
        try:
            balance = await checker.get_balance(address)
            return checker.currency, address, balance
        except Exception as e:
            print(f"Ошибка при получении баланса для {checker.currency} -> {address}: {e}")
            return checker.currency, address, 0
