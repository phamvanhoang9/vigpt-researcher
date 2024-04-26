from colorama import Fore, Style 

"""colorma is the third-party library used for producing colored terminal text and cursor positioning
Fore: this module provides foreground color constants
Style: this module provides style constants like BRIGHT, DIM, NORMAL
"""

print(Fore.GREEN + "This is some green text")
print(Style.BRIGHT + "This is some bright text")
print(Style.RESET_ALL + "This will reset to the default style and color")
