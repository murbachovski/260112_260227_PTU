# 리스트 값 변경과 조작
# 특징 : 순서, 수정, 중복 허용

colors = ["red", "green", "blue"]

# 1. 인덱싱
# print(colors[0]) # red
# print(colors[-1]) # blue

# 2. 슬라이싱
# print(colors[0:2])
# print(colors[0:-1])
# print(colors[1:2])
# ['red', 'green']
# ['red', 'green']
# ['green']

# 3. 값 변경(수정)
# print(colors[-1]) # blue
colors[-1] = "black"
# print(colors[-1]) # black

# 4. 값 추가
colors.append("pink")
# print(colors)
# ['red', 'green', 'black', 'pink']

# 5. 값 추가2
# colors.insert(위치, 값)
colors.insert(0, "white")
# print(colors)
# ['white', 'red', 'green', 'black', 'pink']

# 6. 값 제거
colors.remove("white")
# print(colors)
# ['red', 'green', 'black', 'pink']

numbers = [8, 5, 3, 2, 7, 5, 9]

# 7. 정렬
numbers.sort() # 오름차순 정렬
# print(numbers)
# [2, 3, 5, 5, 7, 8, 9]
numbers.sort(reverse=True) # 내림차순 정렬
# print(numbers)
# [9, 8, 7, 5, 5, 3, 2]

# 8. 뒤집기
numbers.reverse()
# print(numbers)
# [2, 3, 5, 5, 7, 8, 9]

# 9. 리스트 요소 포함 여부 확인
# print(10 in numbers) # False
print(2 in numbers) # True