class GUISymbols:
    """
    Библиотека символов для UV-терминала.
    Содержит псевдографику, геометрические фигуры и другие полезные символы.
    """

    def __init__(self):
        # Псевдографика для построения рамок и таблиц
        self.box_top_left = "┌"       # Левый верхний угол
        self.box_top_right = "┐"      # Правый верхний угол
        self.box_bottom_left = "└"    # Левый нижний угол
        self.box_bottom_right = "┘"   # Правый нижний угол
        self.box_horizontal = "─"     # Горизонтальная линия
        self.box_vertical = "│"       # Вертикальная линия
        self.box_cross = "┼"          # Пересечение линий
        self.box_tee_up = "┬"         # Т-образное соединение сверху
        self.box_tee_down = "┴"       # Т-образное соединение снизу
        self.box_tee_left = "├"       # Т-образное соединение слева
        self.box_tee_right = "┤"      # Т-образное соединение справа

        # Геометрические фигуры
        self.circle = "●"             # Круг
        self.square = "■"             # Квадрат
        self.triangle_up = "▲"        # Треугольник вверх
        self.triangle_down = "▼"      # Треугольник вниз
        self.triangle_left = "◄"      # Треугольник влево
        self.triangle_right = "►"     # Треугольник вправо

        # Маркеры и индикаторы
        self.checkmark = "✔"          # Галочка
        self.cross = "✘"              # Крестик
        self.bullet = "•"             # Маркер списка
        self.star = "★"               # Звезда
        self.diamond = "◆"            # Ромб

        # Стрелки
        self.arrow_up = "↑"           # Стрелка вверх
        self.arrow_down = "↓"         # Стрелка вниз
        self.arrow_left = "←"         # Стрелка влево
        self.arrow_right = "→"        # Стрелка вправо
        self.double_arrow_up = "⇑"    # Двойная стрелка вверх
        self.double_arrow_down = "⇓"  # Двойная стрелка вниз
        self.double_arrow_left = "⇐"  # Двойная стрелка влево
        self.double_arrow_right = "⇒" # Двойная стрелка вправо

        # Разделители и декоративные элементы
        self.divider_thick = "━" * 40  # Толстый разделитель
        self.divider_thin = "─" * 40   # Тонкий разделитель
        self.wave = "≈"                # Волна
        self.dash = "╌"                # Штрих

        # Специальные символы
        self.warning = "⚠"             # Предупреждение
        self.info = "ℹ"                # Информация
        self.smiley = "😊"             # Улыбающееся лицо
        self.sad = "😢"                 # Грустное лицо
        self.gear = "⚙"                # Шестеренка
        self.lightning = "⚡"           # Молния
        self.music_note = "🎵"          # Нота

    def list_symbols(self):
        """
        Возвращает список всех доступных символов с их значениями.
        """
        return {
            "box_top_left": self.box_top_left,
            "box_top_right": self.box_top_right,
            "box_bottom_left": self.box_bottom_left,
            "box_bottom_right": self.box_bottom_right,
            "box_horizontal": self.box_horizontal,
            "box_vertical": self.box_vertical,
            "box_cross": self.box_cross,
            "box_tee_up": self.box_tee_up,
            "box_tee_down": self.box_tee_down,
            "box_tee_left": self.box_tee_left,
            "box_tee_right": self.box_tee_right,
            "circle": self.circle,
            "square": self.square,
            "triangle_up": self.triangle_up,
            "triangle_down": self.triangle_down,
            "triangle_left": self.triangle_left,
            "triangle_right": self.triangle_right,
            "checkmark": self.checkmark,
            "cross": self.cross,
            "bullet": self.bullet,
            "star": self.star,
            "diamond": self.diamond,
            "arrow_up": self.arrow_up,
            "arrow_down": self.arrow_down,
            "arrow_left": self.arrow_left,
            "arrow_right": self.arrow_right,
            "double_arrow_up": self.double_arrow_up,
            "double_arrow_down": self.double_arrow_down,
            "double_arrow_left": self.double_arrow_left,
            "double_arrow_right": self.double_arrow_right,
            "divider_thick": self.divider_thick,
            "divider_thin": self.divider_thin,
            "wave": self.wave,
            "dash": self.dash,
            "warning": self.warning,
            "info": self.info,
            "smiley": self.smiley,
            "sad": self.sad,
            "gear": self.gear,
            "lightning": self.lightning,
            "music_note": self.music_note,
        }


if __name__ == "__main__":
    # Создаем объект библиотеки символов
    symbols = GUISymbols()

    # Пример использования символов
    print(f"{symbols.box_top_left}{symbols.box_horizontal * 10}{symbols.box_top_right}")
    print(f"{symbols.box_vertical} Пример текста {symbols.box_vertical}")
    print(f"{symbols.box_bottom_left}{symbols.box_horizontal * 10}{symbols.box_bottom_right}")

    print(f"\n{symbols.checkmark} Готово!")
    print(f"{symbols.cross} Ошибка!")
    print(f"{symbols.warning} Внимание!")

    # Выводим список всех доступных символов
    print("\nСписок всех символов:")
    for name, symbol in symbols.list_symbols().items():
        print(f"{name}: {symbol}")