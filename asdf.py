class 갓겜:
    def __init__(self, n: str) -> None:
        self.name = n
        self.총과금액 = 0

    def 현질(self, 액수: int):
        self.총과금액 += 액수

game1 = 갓겜("메이플") #__init__의 n에 "메이플"할당
game2 = 갓겜("몬스터디펜스")

game1.총과금액 #0
game1.현질(20000000)
game1.총과금액 # 20000000

A = int(input())
game1.현질(A)
game2.현질(A//2)
print(game1.총과금액)

class 알바:
    def __init__(self, atsui: str) -> None:
        self.알바이름 = atsui
        self.녹봉 = 0

    def 돈주기(self, 미친돈):
        self.녹봉 += 미친돈

    def 돈뺏기(self, 미친돈):
        self.녹봉 -= 미친돈

알바1 = 알바("심준석")
알바2 = 알바('진현준')

print(알바1.녹봉)
# >> 0
알바1.돈주기(20051210)
print(알바1.녹봉)
# >> 20051210

print(알바2.녹봉)
# >> 0
알바2.돈뺏기(20060222)
print(알바2.녹봉)
# >> -20060222
