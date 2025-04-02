import colorama
from colorama import Fore, Back, Style
from .base import BaseEntity
from sys  import stdout

# Инициализация colorama
colorama.init(autoreset=True)



class Logo(BaseEntity):
    def __init__(self, name, description, fill=Fore.WHITE):
        super().__init__(name, description)
        self.fill = fill

    def get_logo_text(self):
        """
        Возвращает текст логотипа.
        """
        return r"""
        ################################################################
        #     .-') _                                             ('-.  #
        #    ( OO ) )                                          _(  OO) #
        #,--./ ,--,'  .-'),-----.  ,--.      ,--.      ,-.-') (,------.#
        #|   \ |  |\ ( OO'  .-.  ' |  |.-')  |  |.-')  |  |OO) |  .---'#
        #|    \|  | )/   |  | |  | |  | OO ) |  | OO ) |  |  \ |  |    #
        #|  .     |/ \_) |  |\|  | |  |`-' | |  |`-' | |  |(_/(|  '--. #
        #|  |\    |    \ |  | |  |(|  '---.'(|  '---.',|  |_.' |  .--' #
        #|  | \   |     `'  '-'  ' |      |  |      |(_|  |    |  `---.#
        #`--'  `--'       `-----'  `------'  `------'  `--'    `------'#
        #                  .-') _  _ .-') _     ('-.  _  .-')          #
        #                 ( OO ) )( (  OO) )  _(  OO)( \( -O )         #
        # ,--. ,--.   ,--./ ,--,'  \     .'_ (,------.,------.         #
        # |  | |  |   |   \ |  |\  ,`'--..._) |  .---'|   /`. '        #
        # |  | | .-') |    \|  | ) |  |  \  ' |  |    |  /  | |        #
        # |  |_|( OO )|  .     |/  |  |   ' |(|  '--. |  |_.' |        #
        # |  | | `-' /|  |\    |   |  |   / : |  .--' |  .  '.'        #
        #('  '-'(_.-' |  | \   |   |  '--'  / |  `---.|  |\  \         #
        #  `-----'    `--'  `--'   `-------'  `------'`--' '--'        #
        #            _  .-')              .-. .-')                     #
        #           ( \( -O )             \  ( OO )                    #
        #  ,----.    ,------.  .-'),-----. ;-----.\                    #
        # '  .-./-') |   /`. '( OO'  .-.  '| .-.  |                    #
        # |  |_( O- )|  /  | |/   |  | |  || '-' /_)                   #
        # |  | .--, \|  |_.' |\_) |  |\|  || .-. `.                    #
        #(|  | '. (_/|  .  '.'  \ |  | |  || |  \  |                   #
        # |  '--'  | |  |\  \    `'  '-'  '| '--'  /                   #
        #  `------'  `--' '--'     `-----' `------'                    #
        ################################################################"""

    def display_logo(self):
        """
        Выводит логотип с настраиваемыми цветами для рамки, текста и других элементов.
        """
        stdout.write(f"""{self.fill}{self.get_logo_text()}{Style.RESET_ALL}""")
        stdout.flush()

    

if __name__ == "__main__":
    my_logo = Logo(name="NollieUndergrob", description="A colorful logo with customizable styles")

    print("Информация о логотипе:")
    my_logo.display()

    print("\nЛоготип с настройками по умолчанию:")
    my_logo.display_logo()

    print("\nЛоготип с красной рамкой, зеленым текстом и синими элементами:")
    custom_logo = Logo(
        name="CustomLogo",
        description="A customized version of the logo",
        fill=Fore.RED
    )
    custom_logo.display_logo()
    custom_logo.display()