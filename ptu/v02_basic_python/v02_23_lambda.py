# 람다 함수 기본 구조
# 함수명 = lambda 매개변수1, 매개변수2 . . . : 실행할 표현식

# 일반 함수
# def add(a, b):
#     return a + b
# sum = add(2, 3)
# print(sum)
# 5

# 람다 함수
add = lambda a, b : a+b
sum = add(7, 3)
print(sum)
# 10

# 람다 함수 사용 이유
# 코드가 간결해집니다 (Conciseness)
# 메모리 효율과 일회성