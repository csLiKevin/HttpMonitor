from colorama import Back, Style, init
init()


def print_error(text):
    print(f"{Back.RED}ERROR{Style.RESET_ALL} {text}")


def print_info(text):
    print(f"{Back.BLUE}INFO{Style.RESET_ALL} {text}")


def print_success(text):
    print(f"{Back.GREEN}SUCCESS{Style.RESET_ALL} {text}")


def print_warning(text):
    print(f"{Back.LIGHTYELLOW_EX}WARNING{Style.RESET_ALL} {text}")
