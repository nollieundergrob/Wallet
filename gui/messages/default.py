import colorama
import sys
import shutil
import itertools


def alert(message, *args, **kwargs):
    """
    This is the alert function
    
    arguments:
        message: str - The main message to display
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments for customization
    
    returns:
        None
    """
    formatted_message = message.format(*args, **kwargs) if args or kwargs else message
    sys.stdout.write(f"\n{colorama.Fore.YELLOW}▉ Alert: {formatted_message}{colorama.Style.RESET_ALL}\n")
    sys.stdout.flush()

def error(message, *args, **kwargs):
    """
    This is the error function
    
    arguments:
        message: str - The main message to display
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments for customization
    
    returns:
        None
    """
    formatted_message = message.format(*args, **kwargs) if args or kwargs else message
    sys.stdout.write(f"\n{colorama.Fore.RED}▉ Error: {formatted_message}{colorama.Style.RESET_ALL}\n")
    sys.stdout.flush()

def warning(message, *args, **kwargs):
    """
    This is the warning function
    
    arguments:
        message: str - The main message to display
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments for customization
    
    returns:
        None
    """
    formatted_message = message.format(*args, **kwargs) if args or kwargs else message
    sys.stdout.write(f"\n{colorama.Fore.YELLOW}▉ Warning: {formatted_message}{colorama.Style.RESET_ALL}\n")
    sys.stdout.flush()

def action(message, *args, **kwargs):
    """
    This is the action function
    
    arguments:
        message: str - The main message to display
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments for customization
    
    returns:
        None
    """
    formatted_message = message.format(*args, **kwargs) if args or kwargs else message
    sys.stdout.write(f"\n{colorama.Fore.CYAN}▉ Action: {formatted_message}{colorama.Style.RESET_ALL}\n")
    sys.stdout.flush()

def success(message, *args, **kwargs):
    """
    This is the success function
    
    arguments:
        message: str - The main message to display
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments for customization
    
    returns:
        None
    """
    formatted_message = message.format(*args, **kwargs) if args or kwargs else message
    sys.stdout.write(f"\n{colorama.Fore.GREEN}▉ Success: {formatted_message}{colorama.Style.RESET_ALL}\n")
    sys.stdout.flush()

def title(message, *args, **kwargs):
    """
    This is the title function
    
    arguments:
        message: str - The main message to display
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments for customization
    
    returns:
        None
    """
    formatted_message = message.format(*args, **kwargs) if args or kwargs else message
    sys.stdout.write(f"\n{colorama.Fore.BLUE}▉ Title: {formatted_message}{colorama.Style.RESET_ALL}\n")
    sys.stdout.flush()

def change(message, *args, **kwargs):
    """
    This is the change function
    
    arguments:
        message: str - The main message to display
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments for customization
    
    returns:
        None
    """
    formatted_message = message.format(*args, **kwargs) if args or kwargs else message
    sys.stdout.write(f"\n{colorama.Fore.MAGENTA}▉ Change: {formatted_message}{colorama.Style.RESET_ALL}\n")
    sys.stdout.flush()

def debug_row(message, *args, **kwargs):
    """
    This is the debug_row function
    
    arguments:
        message: str - The main message to display
        *args: Additional positional arguments for formatting
        **kwargs: Additional keyword arguments for customization
    
    returns:
        None
    """
    formatted_message = message.format(*args, **kwargs) if args or kwargs else message
    sys.stdout.write(f"\n{colorama.Back.WHITE}{colorama.Fore.BLACK}▉ Debug:\n {formatted_message} {colorama.Style.RESET_ALL}\n")
    sys.stdout.flush()




spinner_cycle = itertools.cycle([
    '|','|','|','|','|','|','|','|','|','|','|','|','|','|','|','|',
    '/', '/','/','/','/','/','/','/','/', '/','/','/','/','/','/','/',
    '-','-','-','-','-','-','-','-', '-','-','-','-','-','-','-','-', 
    '\\', '\\', '\\', '\\', '\\', '\\', '\\', '\\','\\', '\\', '\\', '\\', '\\', '\\', '\\', '\\'
    ])

def styled_inline_status(
    message: str,
    prefix: str = "",
    color: str = colorama.Fore.GREEN,
    suffix: str = "",
    animate: bool = True,
    spinner_symbol: str = None
):
    """
    Красиво выводит строку в одну строку с анимацией, центрируя по ширине терминала.
    """
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    spin = spinner_symbol or (next(spinner_cycle) if animate else "")
    text = f"{color}▉ {prefix} {message} {spin} {suffix}{colorama.Style.RESET_ALL}"
    padded = text.center(terminal_width)
    sys.stdout.write(f"\r{padded}")
    sys.stdout.flush()


if __name__ == '__main__':
    alert('This is an alert with {}', 'dynamic content')
    error('Error occurred at line {line}', line=42)
    warning('Warning: {warning_type}', warning_type='deprecated feature')
    action('Action: {action_name}', action_name='processing data')
    success('Success: Processed {count} items', count=100)
    title('Title: {title}', title='Main Menu')
    change('Change: Updated {field} to {value}', field='username', value='admin')
    debug_row('Debug: Variable {var} has value {val}', var='x', val=10)
    alert("{0} {1}", "Hello", "World")