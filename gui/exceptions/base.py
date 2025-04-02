from colorama import Fore,Style
def base_error_message(message, *args, **kwargs):
    """
    Формирует базовое сообщение об ошибке с возможностью форматирования.
    
    arguments:
        message: str - Основное сообщение об ошибке.
        *args: Дополнительные позиционные аргументы для форматирования.
        **kwargs: Дополнительные именованные аргументы для форматирования.
    
    returns:
        str - Отформатированное сообщение об ошибке.
    """
    formatted_message = message.format(*args, **kwargs) if args or kwargs else message
    return f"\n{Fore.RED}▉ Error: {formatted_message}{Style.RESET_ALL}\n"