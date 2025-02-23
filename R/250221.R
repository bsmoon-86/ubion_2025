# 변수 생성
a <- 10
a
b = "test"
TRUE -> c
print(typeof(a))
print(typeof(b))
print(typeof(c))

# 벡터 데이터
# c() 함수를 이용해서 생성
# 일반적인 변수는 데이터를 1개 저장시킨다면
# 벡터 데이터는 같은 타입의 데이터를 여러개 저장
d <- c(1, 2, 3, 4, 5)
e <- c(1, "test")
f <- c(TRUE, "test")

print(d)
print(e)
print(f)

print(e[1])

# 2차원 데이터
arr_x = array(c(1, 2, 3, 4, 5, 6), dim = c(2, 3))
print(arr_x)
arr_y = array(1:10, dim = c(5, 5))
print(arr_y)


# 리스트 형태의 데이터 생성
# R에서는 리스트 형태는 Python에서는 딕셔너리 형태 
# 벡터 데이터에서 index(위치) 값을 기준으로 데이터를 출력한다면
# 리스트에서는 위치 대신에 key 값을 기준으로 데이터를 출력
# 데이터의 순서와 상관없이 데이터를 주고 받는다. 
# 리스트형태는 데이터의 타입이 여러개가 동시에 저장 가능

list_x = list(name = "test", age = 20, phone = "01012345678")
print(list_x)
list_y = list(name = "test2", phone = "01011112222", age = 25)
print(list_y)
print(list_x['age'])
print(list_y['age'])

list_z = list(name = c('test', 'test2', 'test3'),
              age = c(20, 30, 40), 
              phone = c('01011112222', '010112345656', '01099998888'))

print(list_z)
print(list_z['age'])
print(list_z$age[3])

# 데이터프레임 생성
# 인덱스와 컬럼의 이름을 기준으로 데이터를 생성
df = data.frame(
  name = c("test", "test2", "test3"), 
  age = c(20, 30, 40), 
  phone = c("01011112222", "010199998888", "01012345678")
)
print(df)

# 데이터프레임에서 벡터 데이터의 개수가 다르다면 에러 발생
df2 = data.frame(
  name = c('test', 'test2', 'test3'), 
  age = c(20, 30)
)      

# 연산자 

# 산술 연산자 
x <- 10
y <- 3

x + y
print(x + y)
x + y -> z
x - y
x * y
x / y
x ^ y
x %% y
x %/% y

# 비교연산자
# 결과 값이 참/거짓 형태로 출력

x == y
x != y
x > y
x < y
x >= y
x <= y

# 논리 연산자 

# 부정
print(!TRUE)

# and 
# 두 개의 논리값이 모두 참인 경우에만 참을 출력
# 그 외의 경우는 모두 거짓
print(TRUE&TRUE)
print(TRUE&FALSE)

# or
# 두 개의 논리값 중 하나의 논리값이라도 참이라면 참을 출력
# 모두 거짓인 경우에만 거짓을 출력 
print(TRUE|TRUE)
print(TRUE|FALSE)
print(FALSE|FALSE)


# 조건문 
# if문 ( 특정한 조건식에 따라서 실행되는 코드를 구분 )
x <- 10
if (x > 5){
  # x가 5보다 큰 경우 실행이 되는 부분
  print("x는 5보다 크다")
}

y <- 3
if(y > 5){
  print('y는 5보다 크다')
}

# if ~ else 구문
# if 조건식이 참인 경우 실행할 코드 
# else는 거짓인 경우 실행할 코드 
if (y > 5){
  # 조건식이 참인 경우
  print('y는 5보다 크다')
}else {
  # 조건식이 거짓인 경우
  print('y는 5보다 작거나 같다')
}

score <- 85

# A 학점의 기준은 90점 이상
if (score >= 90){
  print('A')
}
# B 학점의 기준은 80점 이상 90점 미만
if (score >= 80 & score < 90 ){
  print('B')
}
# C 학점의 기준은 70점 이상 80점 미만
if (score >= 70 & score < 80){
  print('C')
}


if (score >= 90){
  print('A')
}else if (score >= 80){
  print('B')
}else if (score >= 70){
  print('C')
}else {
  print('F')
}

# 로그인의 과정 
# id와 password가 모두 일치해야 로그인이 성공
id <- 'test'
pass <- '1111'
if (id == 'test' & pass == '1234'){
  print('로그인 성공')
}else{
  print('로그인 실패')
}

# 특정한 입력값이 7의 배수인지 판단을 하는 조건문을 생성 
x <- 8845
# 조건식 x를 7로 나눈 뒤 나머지가 0이라면
if (x %% 7 == 0){
  print('x는 7의 배수이다.')
}else {
  print('x는 7의 배수가 아니다.')
}
x %% 7

# which문 
# 벡터데이터에서 조건식에 일치하는 데이터의 index 값을 출력 
names <- c('test', 'test2', 'test3')

which(names == 'test2')

if (names[1] == 'test2'){
  print(1)
}else if (names[2] == 'test2'){
  print(2)
}else if (names[3] == 'test2'){
  print(3)
}
which ( names != 'test2' )

# 반복문 
# for문 
for ( i in 1:10 ){
  print(i)
}

1+2+3+4+5+6+7+8+9+10

# 1부터 10까지의 합을 구하는 반복문 

# 합계라는 변수를 생성해서 데이터는 0을 저장 
result = 0
# 1부터 10까지 반복 실행하는 반복문을 생성 
for ( i in 1:10 ){
  # result와 i를 더한다. 
  result + i -> result
  print(result)
}
print(result)


# break문 : 반복문을 강제로 종료
for ( i in 1:10 ){
  if (i > 5){
    break
  }
  print(i)
}
for ( i in 1:10 ){
  print(i)
  if ( i > 5 ){
    break
  }
}

# 1부터 1씩 증가시킨 값을 누적합하였을때 
# 처음으로 5000을 넘어가는 지점은 어디인가?
result = 0
for ( i in 1:1000 ){
  result = result + i
  if (result >= 5000){
    break
  }
}
print(result)
print(i)

result = 0
for ( i in 1:1000 ){
  if (result >= 5000){
    break
  }
  result = result + i
}
print(i)
print(result)

for (i in c('test', 'test2', 'test3')){
  print(i)
}

# 2차원 데이터를 가지고 반복문을 이용 
arr_x = array(1:10, dim = c(2, 5))
arr_x

for ( i in arr_x ){
  print(i)
}

df = data.frame(
  a = c(1,2,3), 
  b = c(6,7,8)
)
df
result = 0
for ( i in df){
  # i는 1차원 백터데이터
  # print(i)
  for ( j in i){
    print(j)
    result = result + j
  }
}
print(result)


# while문 
i = 1
while (i <= 10){
  print(i)
  i = i + 1
}

# while문을 이용한 무한루프 사용법 
# 1부터 누적합이 1억이 넘어가는 시점을 찾아보자 
result = 0
i = 1

# 무한루프 
while (TRUE){
  result = result + i
  # 증가식 
  i = i + 1
  # 누적합이 1억 이상일때 반복문을 강제 종료
  if (result >= 100000000){
    print(i)
    print(result)
    break
  }
}

result = 0
i = 1

# 무한루프 
while (TRUE){  
  # 누적합이 1억 이상일때 반복문을 강제 종료
  if (result >= 100000000){
    print(i)
    print(result)
    break
  }
  result = result + i
  # 증가식 
  i = i + 1

}
