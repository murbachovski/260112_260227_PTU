# termcolor를 활용한 텍스트 출력 함수 실습

from termcolor import colored

# 함수 정의
def print_colored(sentence:str="Default", color:str="red", on_color:str="on_green", style:list=["bold"]):
    '''
    텍스트를 원하는 색상, 배경색, 스타일로 출력하는 함수
    
    매개 변수:
    sentence(str) : 출력할 문자열
    color(str) : 글자 색상
    on_color(str) : 글자 배경색
    style(list) : 글자 스타일
    '''
    color_sentence = colored(sentence,
                             color,
                             on_color,
                             style
                             )
    print(color_sentence)

print_colored()