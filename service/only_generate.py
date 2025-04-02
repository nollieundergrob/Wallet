import time
from gui.messages.default import success, error, action,styled_inline_status
from pathlib import Path
from service.mnemonic_service import BIP39WalletApp
from utils.system_utils import clear_console

def format_duration(seconds: float) -> str:
    """Форматирует секунды в строку вида: 1 ч 2 мин 3 сек"""
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours} ч")
    if minutes > 0:
        parts.append(f"{minutes} мин")
    if hours == 0:  # только если нет часов — показываем секунды
        parts.append(f"{seconds} сек")
    
    return ' '.join(parts)

async def run_only_generate_txt(count: int = 10, coin: str = "BTC", out_file: str = "private_keys.txt", data_type: str = 'private_key'):
    clear_console()
    app = BIP39WalletApp()
    path = Path("export") / out_file
    path.parent.mkdir(parents=True, exist_ok=True)

    start_time = time.time()

    with path.open("a", encoding="utf-8") as f:
        for i in range(1, count + 1):
            try:
                data = app.create_wallet_data(coin=coin)
                value = data[data_type]
                f.write(value + "\n")
                # action(f"[{i}] Сгенерирован {data_type}")
            except Exception as e:
                error(f"[{i}] Ошибка генерации: {e}")
                continue

            # оценка оставшегося времени
            elapsed = time.time() - start_time
            avg_per_item = elapsed / i
            remaining = (count - i) * avg_per_item

            styled_inline_status(f"⏳ Осталось ~ {format_duration(remaining)} ({i}/{count}) {i*100/count:.2f}%)")

    total_time = time.time() - start_time
    success(f"✅ {count} {data_type} сохранены в {path} за {format_duration(total_time)}")
