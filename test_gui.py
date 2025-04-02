from gui.entity.logo import Logo
from gui.symbols.ascii import GUISymbols
from gui.messages.default import (alert,warning,action,title,change,error,debug_row)
from gui.messages.framed import FramedMessage
from gui.exceptions.ItrenalAppException import ItrenalAppException
from gui.entity.menu import Menu

from colorama import Fore,Back,Style

logo = Logo(
    name='Nollieundergrob',
    description='Test',
)
symbols = GUISymbols()

logo.display_logo()
logo.display()

alert('This is an alert message.')
warning(f'{symbols.warning} This is a warning message.')
action('This is an action message.')
error('This is an error message.')
title('This is a title message.')
change('This is a change message.')
debug_row(f'A graphical user interface, or GUI {symbols.bullet}{symbols.checkmark}, is a form of user interface that allows users to interact with electronic devices through graphical icons and visual indicators such as secondary notation. In many applications, GUIs are used instead of text-based UIs, which are based on typed command labels or text navigation.')

import datetime
try:
    raise ItrenalAppException('This is a test exception. debug:{debug} exit:{exit},time',{"debug":True, "exit":True, "time":datetime.datetime.now()},debug=True, exit=True)
except ItrenalAppException as e:
    print(e)

framed = FramedMessage(
    padding=2,
)

print(framed.create_frame('Hello world'))
print(symbols.list_symbols())

menu =Menu(title='Загловок меню')
colors = [
    Fore.BLACK,
    Fore.BLUE,
    Fore.CYAN,
    Fore.GREEN,
    Fore.MAGENTA,
    Fore.RED,
    Fore.RED,
]
import random
for i in range(10):
    menu.add_item(random.choice(colors)+"Пункт меню",random.choice(colors))
    
menu.display()
choice = menu.get_choice()
print(choice)
import datetime
try:
    print(100010/0)
except Exception as e:
    raise ItrenalAppException('Ошибка0',{
        'exception':e,
        'args':e.args,
        'message':e.__str__(),
        'exception_type':type(e).__name__,
        'exception_module':type(e).__module__,
        'exception_doc':e.__doc__,
        'exception_str':str(e),
        'exception_repr':repr(e),
        'line':e.__traceback__.tb_lineno,
        'exception_format':format(e),
        'traceback':e.__traceback__,
        'time':datetime.datetime.now(),
        },debug=True)
