from termcolor import colored

# colored(출력할 문자열, 글자색, 배경색, atts=[스타일])

color_sentence = colored(
    "Hello",
    "red",
    "on_green",
    # ["bold"]
    ["bold", "reverse"]
)
print(color_sentence)