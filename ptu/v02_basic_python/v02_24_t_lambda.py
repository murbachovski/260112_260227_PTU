# ============
# pyfiglet + 함수 + lambda 함수
# ============
import pyfiglet

# 일반 함수 정의
# def decorate_text(text):
#     py_text = pyfiglet.figlet_format(text)
#     print(py_text)

# decorate_text("Hello")

decorate_text = lambda text: pyfiglet.figlet_format(text)
py_text = decorate_text("Lambda")
print(py_text)