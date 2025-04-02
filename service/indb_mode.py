import aiosqlite
from gui.messages.default import success, error, action, title
from service.mnemonic_service import BIP39WalletApp

from pathlib import Path
import json
import asyncio
import datetime

DB_FILE = Path("databases/wallets.db")

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS wallet (
    wallet_id INTEGER PRIMARY KEY AUTOINCREMENT,
    coin TEXT,
    address TEXT UNIQUE,
    private_key TEXT,
    public_key TEXT,
    mnemonic TEXT,
    seed TEXT,
    path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS status_wallet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wallet_id INTEGER,
    status TEXT CHECK(status IN ('unchecked', 'checked')),
    FOREIGN KEY(wallet_id) REFERENCES wallet(wallet_id)
);
CREATE TABLE IF NOT EXISTS ping_wallet (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wallet_id INTEGER,
    url_resource TEXT,
    status_code INTEGER,
    json_response TEXT,
    pinged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(wallet_id) REFERENCES wallet(wallet_id)
);
"""

async def setup_database():
    async with aiosqlite.connect(DB_FILE) as db:
        await db.executescript(CREATE_TABLES_SQL)
        await db.commit()

async def run_indb_generate(count: int = 10, coin: str = "BTC"):
    await setup_database()
    app = BIP39WalletApp()

    async with aiosqlite.connect(DB_FILE) as db:
        for _ in range(count):
            data = app.create_wallet_data(coin=coin)
            await db.execute("""
                INSERT INTO wallet (coin, address, private_key, public_key, mnemonic, seed, path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (coin, data["address"], data["private_key"], data["public_key"], data["mnemonic"], data["seed"], data["path"]))
                

            # Получаем ID для связи
            cursor = await db.execute("SELECT wallet_id FROM wallet WHERE address = ?", (data["address"],))
            row = await cursor.fetchone()
            wallet_id = row[0]

            await db.execute("INSERT INTO status_wallet (wallet_id, status) VALUES (?, 'unchecked')", (wallet_id,))
            await db.commit()

            success(f"{_}/{count} [DB] Сохранен кошелек {data['address']}")
async def run_indb_ping(proxy: str = None):
    from service.balance import (
        AsyncBlockstreamBalanceChecker,
        AsyncLitecoinMultiChecker,
        AsyncDogecoinMultiChecker,
        AsyncEtherscanBalanceChecker
    )

    await setup_database()

    checker_map = {
        "BTC": AsyncBlockstreamBalanceChecker(proxy=proxy),
        "LTC": AsyncLitecoinMultiChecker(proxy=proxy),
        "DOGE": AsyncDogecoinMultiChecker(proxy=proxy),
        "ETH": AsyncEtherscanBalanceChecker(api_key="YOUR_ETHERSCAN_API_KEY", proxy=proxy),
    }

    async with aiosqlite.connect(DB_FILE) as db:
        cursor = await db.execute("""
            SELECT w.wallet_id, w.address, w.coin
            FROM wallet w
            JOIN status_wallet s ON w.wallet_id = s.wallet_id
            WHERE s.status = 'unchecked'
        """)
        rows = await cursor.fetchall()

        if not rows:
            action("Нет непроверенных кошельков в базе.")
            return

        for wallet_id, address, coin in rows:
            checker = checker_map.get(coin)
            if not checker:
                error(f"[SKIP] Нет чекера для валюты {coin}")
                continue

            try:
                balance = await checker.get_balance(address)
                await db.execute("""
                    INSERT INTO ping_wallet (wallet_id, url_resource, status_code, json_response)
                    VALUES (?, ?, ?, ?)
                """, (
                    wallet_id,
                    checker.BASE_URL,
                    200,
                    json.dumps({"balance": balance})
                ))

                await db.execute("""
                    UPDATE status_wallet SET status = 'checked' WHERE wallet_id = ?
                """, (wallet_id,))
                await db.commit()

                action(f"[✓] {coin} {address} → {balance / 1e8:.8f}" if coin != "ETH" else f"[✓] {coin} {address} → {balance} ETH")

            except Exception as e:
                error(f"[FAIL] {coin} {address} — {str(e)}")


