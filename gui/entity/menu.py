import colorama
from colorama import Fore, Style

# Инициализация colorama
colorama.init(autoreset=True)

class Menu:
    """
    Класс для создания и управления текстовым меню.
    """

    def __init__(self, title="Меню"):
        """
        Инициализация объекта Menu.

        arguments:
            title: str - Заголовок меню (по умолчанию "Меню").
        """
        self.title = title
        self.items = []  

    def add_item(self, item_name, item_color=Fore.WHITE):
        """
        Добавляет пункт в меню с указанным цветом для символа ▉.

        arguments:
            item_name: str - Название пункта меню.
            item_color: str - Цвет для символа ▉ (например, Fore.RED).

        returns:
            None
        """
        self.items.append((item_name, item_color))

    def display(self):
        """
        Выводит все пункты меню с автонумерацией и цветными символами ▉.

        returns:
            None
        """
        print(f"{Fore.CYAN}{self.title}:")
        for index, (item_name, item_color) in enumerate(self.items, start=1):
            print(f"{item_color}▉\t{Fore.YELLOW}{index}. {Fore.WHITE}{item_name}")

    def get_choice(self):
        """
        Ожидает выбор пользователя и возвращает полное название выбранного пункта.

        returns:
            str - Полное название выбранного пункта.
        """
        while True:
            try:
                choice = input(f"{Fore.GREEN}Введите номер пункта: {Style.RESET_ALL}")
                choice_index = int(choice) - 1  
                if 0 <= choice_index < len(self.items):
                    return self.items[choice_index][0]  
                else:
                    print(f"{Fore.RED}Ошибка: Введите номер из доступных пунктов.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Ошибка: Пожалуйста, введите число.{Style.RESET_ALL}")


if __name__ == "__main__":
    # Пример использования класса Menu
    menu = Menu(title="Главное меню")
    menu.add_item("Начать игру", Fore.GREEN)
    menu.add_item("Настройки", Fore.BLUE)
    menu.add_item("Выход", Fore.RED)

    menu.display()
    selected_item = menu.get_choice()
    print(f"{Fore.MAGENTA}Вы выбрали: {selected_item}{Style.RESET_ALL}")