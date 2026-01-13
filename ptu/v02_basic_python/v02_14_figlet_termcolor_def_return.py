import pyfiglet
from termcolor import colored

# 1. 함수 정의
def decorate_text(text, color):
    '''
    1. pyfiglet으로 텍스트를 튜닝
    2. termcolor로 색상 적용
    '''
    py_text = pyfiglet.figlet_format(text)
    color_py_text = colored(py_text, color)
    # print(color_py_text)
    return color_py_text

# 2. 함수 호출
decorate_text("GOOD", "red")

# 1. 텍스트 출력 완성
# print(decorate_text("GOOD", "red"))
# print_text = decorate_text("GOOD", "red")
# print(print_text)

# 2. return을 사용하는 이유
    # 1. 함수의 실행 결과 값을 함수 밖으로 전달할 수 있음
    # 2. 함수 재사용성과 확장성이 높아짐
last_text = decorate_text("LAST", "yellow")

def box_print(text):
    print("=" * 40)
    print(text)
    print("=" * 40)

box_print(last_text)
# ========================================
#  _        _    ____ _____
# | |      / \  / ___|_   _|
# | |     / _ \ \___ \ | |
# | |___ / ___ \ ___) || |
# |_____/_/   \_\____/ |_|
# ========================================