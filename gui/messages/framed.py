import colorama
from colorama import Fore, Back, Style

# Инициализация colorama
colorama.init(autoreset=True)

class FramedMessage:
    """
    Класс для создания сообщений в полностью настраиваемой рамке.
    """

    def __init__(self, padding=1, border_color=Fore.YELLOW, text_color=Fore.WHITE, bg_color=''):
        """
        Инициализация объекта FramedMessage.

        arguments:
            padding: int - Отступ между текстом и рамкой (по умолчанию 1).
            border_color: str - Цвет рамки (например, Fore.CYAN).
            text_color: str - Цвет текста (например, Fore.WHITE).
            bg_color: str - Цвет фона текста (например, Back.BLACK).
        """
        self.padding = padding
        self.border_color = border_color
        self.text_color = text_color
        self.bg_color = bg_color

    def create_frame(self, message):
        """
        Создает сообщение в рамке.

        arguments:
            message: str - Текст сообщения.

        returns:
            str - Сообщение в рамке.
        """
        box_top_left = "┌"
        box_top_right = "┐"
        box_bottom_left = "└"
        box_bottom_right = "┘"
        box_horizontal = "─"
        box_vertical = "│"
        lines = message.split("\n")
        max_line_length = max(len(line) for line in lines)


        top_border = f"{self.border_color}{box_top_left}{box_horizontal * (max_line_length + 2 * self.padding)}{box_top_right}{Style.RESET_ALL}"


        bottom_border = f"{self.border_color}{box_bottom_left}{box_horizontal * (max_line_length + 2 * self.padding)}{box_bottom_right}{Style.RESET_ALL}"

    
        framed_lines = []
        for line in lines:
            padded_line = f"{self.text_color}{self.bg_color}{' ' * self.padding}{line.ljust(max_line_length)}{' ' * self.padding}{Style.RESET_ALL}"
            framed_line = f"{self.border_color}{box_vertical}{Style.RESET_ALL}{padded_line}{self.border_color}{box_vertical}{Style.RESET_ALL}"
            framed_lines.append(framed_line)

        framed_message = [top_border] + framed_lines + [bottom_border]
        return "\n".join(framed_message)


if __name__ == "__main__":
    framed_message = FramedMessage(
        padding=2,
        border_color=Fore.YELLOW,
        text_color=Fore.WHITE,
        bg_color=''
    )

    message = """Привет, это сообщение в рамке!
Вы можете настроить цвета, отступы и стиль.
Это очень удобно для UV-терминала."""
    print(framed_message.create_frame(message))