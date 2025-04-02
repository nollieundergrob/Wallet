import colorama
from colorama import Fore, Style
from .base import base_error_message
colorama.init(autoreset=True)

class ItrenalAppException(Exception):
    def __init__(self, message, extra_info=None, *args, **kwargs):
        """
        Кастомное исключение с поддержкой форматирования и дополнительной информацией.
        
        arguments:
            message: str - Основное сообщение об ошибке.
            extra_info: dict - Дополнительная информация об ошибке (например, код ошибки, время).
            *args: Дополнительные позиционные аргументы для форматирования.
            **kwargs: Дополнительные именованные аргументы для форматирования.
        """
        # Форматируем основное сообщение
        formatted_message = base_error_message(message, *args, **kwargs)
        
        # Инициализация родительского класса Exception
        super().__init__(formatted_message)
        
        # Сохраняем дополнительную информацию
        self.extra_info = extra_info

    def __str__(self):
        """
        Переопределяем метод __str__ для красивого вывода исключения.
        """
        error_message = super().__str__()
        
        if self.extra_info:
            # Format extra information with colorama styles
            extra_info_str = "\n".join(
                f"{Fore.YELLOW}{key}: {value}{Style.RESET_ALL}" 
                for key, value in self.extra_info.items()
            )
            # Replace newlines in extra_info_str outside the f-string
            formatted_extra_info = extra_info_str.replace("\n", "\n  |")
            return (f"{error_message}\n"
                    f"{Fore.CYAN}▉ Additional Information:{Style.RESET_ALL}\n"
                    f"  |{formatted_extra_info}")
        
        return f"{Fore.RED}{error_message}"


if __name__ == "__main__":

        raise ItrenalAppException(
            "Произошла ошибка при выполнении операции {operation}", 
            {"code": 400, "time": "12:34", "details": "Invalid input"}, 
            operation="processing"
        )
