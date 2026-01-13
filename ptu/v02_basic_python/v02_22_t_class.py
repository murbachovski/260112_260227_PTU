# 클래스 실습 예제
# 조건 :
# 1) 생성자 파라미터 self 제외 4개
# 2) 메서드 총 2개 이상
# 3) 객체 3개 생성 

# 클래스 정의
class Car:
    '''
    차량에 대한 클래스야
    '''
    # 생성자
    def __init__(self, name, brand, year, color):
        # 속성
        self.name = name
        self.brand = brand
        self.year = year
        self.color = color
        
    # 메서드 1: 자동차 정보 출력
    def info(self):
        print(f"이름 : {self.name}, 브랜드 : {self.brand}, 년식 : {self.year}년식, 색상: {self.color}")
    
    # 메서드 2: 자동차 운전
    def drive(self):
        print(f"{self.name} 달립니다!!")

# 객체 생성
car1 = Car("소나타", "현대", "2026", "화이트")
car2 = Car("모델S", "테슬라", "2025", "블랙")
car3 = Car("911", "포르쉐", "2020", "레드")

# 메서드 호출
car1.info()
# 이름 : 소나타, 브랜드 : 현대, 년식 : 2026년식, 색상: 화이트
car1.drive()
# 소나타 달립니다!!

car3.info()
# 이름 : 911, 브랜드 : 포르쉐, 년식 : 2020년식, 색상: 레드
car3.drive()
# 911 달립니다!!