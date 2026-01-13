import pyfiglet
from termcolor import colored

# 1. 튜닝 
py_sentence = pyfiglet.figlet_format("Hello")

# 2. 색상
color_py_sentence = colored(py_sentence, "red")

print(color_py_sentence)
#  _   _      _ _       
# | | | | ___| | | ___
# | |_| |/ _ \ | |/ _ \
# |  _  |  __/ | | (_) |
# |_| |_|\___|_|_|\___/