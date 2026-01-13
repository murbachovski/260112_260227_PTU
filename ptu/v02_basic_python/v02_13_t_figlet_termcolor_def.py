# pyfiglet + termcolor를 활용한 텍스트 출력 함수
import pyfiglet
from termcolor import colored

# 1. 함수 정의(독스트링, 타입 힌트, 기본 값 설정)
def decorate_text(text:str, color:str):
    """
    함수 설명
    
        1. pyfiglet으로 텍스트를 튜닝
        2. termcolor로 색상 적용
    매개 변수
    
        text (str) : 출력할 문자열
        color (str) : 글자 색상 (예: 'red', 'green' . . .)
    """
    py_text = pyfiglet.figlet_format(text)
    color_py_text = colored(py_text, color)
    print(color_py_text)
    
# 2. 함수 호출
decorate_text("Hello", "red")
