# 반복문 문제 
# 2개의 주사위를 굴린다. 
# 두개의 주사위의 합이 10인 경우의 수를 모두 출력하시오

# 첫번째 반복문 ( 반복횟수 : 6회 )
for (i in c(1,2,3,4,5,6)){
  # 두번째 반복문 ( 반복횟수 : 6회 )
  for (j in 1:6){
    # 조건문 생성 ( 조건식 : 두 주사위의 합이 10 )
    if (i + j == 10){
      # 조건식이 참이라면 -> 2개의 주사위의 값을 출력한다. 
      print(c(i,j))
    }
  }
}

# while문으로 작성 

# 초기값을 지정 ( 두개의 주사위 초기값 지정 )
i = 1
j = 1

# while문 시작 : 첫번째 주사위의 조건
while (i < 7){
  # 두번째 while문 : 두번째 주사위의 조건 
  while (j <= 6){
    # print(c(i,j))
    # 두 주사위의 합이 10이라는 조건문 생성 
    if(i + j == 10){
      print(c(i, j))
      # 1( 무한루프)
    }
    # 2
    j = j + 1
  }
  # j 값의 초기화
  j = 1
  i = i + 1
}

# 함수
# 특정한 행동을 하는 코드 
# 입력 값을 받아서 특정 행동을 한다. 

# 매개변수, 인자가 존재하지 않는 함수 생성 
func_1 <- function(){
  print('Hello R')
}

# 함수 호출 
func_1()
# 매개변수가 존재하지 않는 함수에 인자값을 넣으면? -> 에러 발생
func_1("test")

# 매개변수가 존재하는 함수를 생성 
func_2 = function(x, y){
  # 입력받은 두개의 값을 더해서 되돌려준다. 
  result = x + y
  return (result)
}
# 매개변수가 존재하는 함수를 호출 
func_2(10, 5)

func1_r = func_1()
func2_r = func_2(10, 5)

print(x)

# 매개변수에 기본값을 설정한 함수 생성 
func_3 = function(x, y = 5){
  result = x ^ y
  return (result)
}

# 매개변수가 2개 -> 인자 2개 
func_3(4)
func_3(4, 2)
# 매개변수에 기본값이 설정 안되어있는 함수는 인자를 
# 모두 적어야된다. 
func_2(4)

# 매개변수가 3개 기본값이 2개 설정 
func_4 = function(x, y = 2, z = 3){
  result = (x + y) ^ z
  return (result)
}

func_4(3)
# func_4()에서 매개변수 x와 z에 값을 입력
func_4(2, 2, 6)
func_4(2, z = 6)

# 입력 값이 가변인 경우
func_5 = function(...){
  print(c(...))
}
func_5(1,3,4,7)

# 다수의 인자 값을 모두 더해서 결과를 돌려주는 함수 
sum_func = function(...){
  # 반복문을 이용해서 다수의 인자 값을 모두 더해준다. 
  # 합계라는 초기값을 생성 0 대입 
  result = 0
  for (i in c(...)){
    result = result + i
  }
  return (result)
}
sum_func(1, 3, 5, 7, 9)
sum_func(1, 3, 5)

sum_func2 = function(x){
  result = 0
  for (i in x){
    result  = result + i
  }
  print(result)
}
sum_func2(c(1,3,5))

# 함수에서 시작값과 종료값을 입력 받아서 누적합을 구하는 함수 
sum_func3 = function(start, end, add_value = 1){
  # 합계라는 초기값 지정 
  result = 0
  # 조건문 
  if (start < end){
    s = start
    e = end
  }else{
    s = end
    e = start
  }
  # while 문으로 합계
  i = s
  # while 조건식
  while (i <= e){
    result = result + i
    i = i + add_value
  }
  return (result)
}
sum_func3(1, 10)
sum_func3(10, 1)
sum_func3(1, 10, 3)

# 인자의 개수가 가변인 평균을 구하는 함수 생성 
mean_func = function(...){
  # 평균 = 합계 / 개수
  # 합계라는 초기값 지정 (0)
  sum_value = 0
  # 개수라는 초기값 지정 (0)
  cnt = 0
  # 반복문 생성
  for ( i in c(...) ){
    # 누적합
    sum_value = sum_value + i
    # 개수의 카운터를 1씩 증가
    cnt = cnt + 1
  }
  # 평균 구하기 
  result = sum_value / cnt
  return (result)
}
mean_func(1,2,3,4,5)


mean_func2 = function(...){
  sum_value = sum(c(...))
  len_value = length(c(...))
  result = sum_value / len_value
  return (result)
}
mean_func2(1,2,3,4,5)

# 커스텀 연산자
"%s%" = function(x, y){
  result = (x + y) ^ y
  return (result)
}

8 %s% 2


# 데이터프레임 
names = c('test', 'test2', 'test3')
grade = c(1, 2, 2)
# 벡터데이터를 이용해서 데이터프레임 생성 
student = data.frame(names, grade)
student

midturm = c(70, 80, 90)
final = c(100, 90, 95)
score = cbind(midturm, final)
score

total = midturm + final
total
midturm + 5

students = data.frame(student, score, total)
students

# 데이터프레임에 새로운 컬럼을 추가 (파생변수 생성)
gender = c('M', 'F', 'F')
# cbind() 함수를 이용할때는 원소의 개수가 같아야된다. 
cbind(students, gender) -> students

# 필터링 
# 특정 컬럼을 확인하는 방법 
# $컬럼명
# [[컬럼명]]
# [[컬럼의 인덱스]]
students$grade
students[['midturm']]
students[[4]]

# [인덱스의 조건, 컬럼의 조건]
students[, 'midturm']
students[1,]
students[1:3, ]
students[c(1,3), ]
students[c(1, 3), c('midturm', 'final')]

# 중간 성적인 80점 이상인 학생의 데이터를 확인 
students$midturm >= 80
students[students$midturm >= 80, ]

flag = students$midturm >= 80
students[flag, 'names']

# 행의 추가(데이터프레임의 컬럼이 같은 데이터를 결합)
new_student = data.frame(
  names = 'test4', 
  gender = 'M', 
  grade = 3, 
  midturm = 60, 
  final = 70, 
  total = 130
)
new_student

rbind(students, new_student) -> students

# 오름차순 정렬 : order()
order(students$midturm)

students[order(students$midturm), ]

# 내림차순 정렬 
order(students$midturm, decreasing = TRUE)
order(-students$midturm) -> flag2

students[flag2, ]


# 외부의 데이터를 로드 (파일 데이터를 로드)
# read.csv()함수
# 인자 값 -> 파일의 위치(경로)

# 절대 경로 
  # 절대적인 주소
  # 환경(컴퓨터가 변한다.)이 변하더라도 같은 위치를 지정 
  # ex) window -> c:/users/admin/document/a.csv
  #     mac -> ~/admin/document/a.csv
  #     web -> https://www.google.com
# 상대 경로
  # 상대적인 주소
  # 환경에 따라서 경로가 변할 수 있다. 
  # 현재 위치에서 상위나 하위 폴더로 이동하여 경로 생성
  # ./ : 현재 위치
  # ../ : 상위 폴더로 이동 (부모 폴더)
  # 폴더명/ : 하위 폴더로 이동 (자식 폴더)

# 상대 경로를 이용하여 데이터 로드 
# 현재 위치(./) -> data라는 하위 폴더로 이동(data/)
# -> csv_exam.csv 파일 선택
df = read.csv("./data/csv_exam.csv")
df
# 절대 경로를 이용하여 데이터 로드 
df2 = read.csv("C:\\ubion_2025\\R\\data\\csv_exam.csv")
df2

# 데이터프레임의 상위만 출력 
head(df)
df[1:6, ]
head(df, 2)
# 데이터프레임의 하위만 출력
tail(df)
tail(df, 2)
# 데이터프레임의 크기 출력 
dim(df)
# 데이터프레임의 기본 정보 출력 
str(df)
# 데이터프레임을 뷰어창에 확인 
View(df)
# view(df)
# 통계 요약 정보 출력
summary(df)

# 수학, 영어, 과학 성적은 모두 더하여 
# 새로운 컬럼을 생성
df$math + df[['english']] + df[[5]] -> df$total
head(df)

# total을 이용해서 평균 점수 컬럼을 생성 
df$total / 3 -> mean_score
cbind(df, mean_score) -> df

# mean_score가 65점 초과라면 'pass'
# 65점 미만이라면 'fail'
# 65점이라면 'hold'
# ifelse()함수를 이용
# ifelse( 조건식 , 참인경우 결과, 거짓인 경우 결과 )
ifelse(
  df$mean_score > 65, 
  'pass', 
  ifelse(
    df$mean_score == 65, 
    'hold', 
    'fail'
  )
) -> df$check
head(df)

# 외부의 패키지 설치 
install.packages('dplyr')
# 패키지 로드 
library(dplyr)

# 컬럼의 이름을 변경 
# rename()함수 
head(df)
rename(df, mean = mean_score) -> df

# 파이프 연산자 %>% -> shift + ctrl + m / command + shift + m

head(df)
df %>% head()

df <- read.csv('./data/csv_exam.csv')

# filter(조건식) : 인덱스 조건식으로 인덱스 필터
df %>% 
  filter(class == 1)

# 기본 
df[df$class == 1, ]

# select(조건식) : 컬럼의 조건식으로 컬럼 필터 
df %>% 
  select(math : science)
# 특정 컬럼을 제외하는 방법
df %>% 
  select(-class)

# class가 3인 데이터들 중에 (인덱스의 조건)
# math, english 성적을 확인 (컬럼의 조건)
# 패키지
df %>% 
  filter(class == 3) %>% 
  select(math, english)
# 기본
df[df$class == 3, c('math', 'english')]

# 차순정렬 
# arrange()
# 오름차순 정렬
df %>% 
  arrange(math)
# 내림차순 정렬
df %>% 
  arrange(desc(math))
df %>% 
  arrange(-math)

# 그룹화 
# group_by()
df %>% 
  group_by(class) %>% 
  summarise(mean_math = mean(math))

# 데이터프레임의 결합 
# 유니언 결합 (단순하게 행을 결합 )

df_1 = data.frame(
  id = 1:3, 
  score = c(80, 70, 90)
)
df_2 = data.frame(
  id = 2:5, 
  weight = c(60, 70, 75, 80)
)
# rbind() 컬럼의 구조가 같은 데이터프레임이 결합
rbind(df_1, df_2)

df_1 %>% 
  bind_rows(df_2)

# 조인결합 
# 특정한 조건에 맞게 데이터프레임을 결합(열을 결합)
# df_1 id는 1, 2, 3
# df_2 id는 2, 3, 4, 5

# 두개의 데이터프레임이 공통적으로 가지고 있는 데이터들의 결합 
inner_join(df_1, df_2, by='id')
# 왼쪽 데이터프레임을 기준으로 조인 결합 
left_join(df_1, df_2, by='id')
# 오른쪽 데이터프레임을 기준으로 조인 결합
right_join(df_1, df_2, by='id')
# 두개의 데이터프레임의 모든 정보를 가지고 결합 
full_join(df_1, df_2, by='id')

df_1 %>% 
  inner_join(df_2, by='id')

df_3 = data.frame(
  id = c(2, 5), 
  gender = c(1, 2)
)
# 3개의 데이터프레임을 단순 행 결합(유니언 결합)
bind_rows(df_1, df_2, df_3)
# 3개의 데이터프레임을 조인 결합 
inner_join(df_1, df_2, df_3, by='id')
# case1
inner_join(
  inner_join(df_1, df_2, by='id'), 
  df_3, 
  by='id'
)
# case2 (파이프)
df_1 %>% 
  inner_join(df_2, by='id') %>% 
  inner_join(df_3, by='id')

library(ggplot2)

midwest = ggplot2::midwest

head(midwest)
str(midwest)
View(midwest)

# poptotal컬럼의 이름을 total로 변경 
# popasian컬럼의 이름을 asian으로 변경
# rename() -> 패키지에 존재 
rename(midwest, asian = popasian, total = poptotal)

midwest %>% 
  rename(asian = popasian) %>% 
  rename(total = poptotal)

# 컬럼의 이름을 변경 
# 특정 컬럼을 선택(county, total, asian)
# 파생변수 생성 (ratio) -> (asian / total) * 100
# ratio 컬럼의 내림차순 정렬 
# 상위 5개 -> head(5)
midwest %>% 
  rename(asian = popasian, total = poptotal) %>% 
  select(county, total, asian) %>% 
  mutate(ratio = (asian / total)*100 ) %>% 
  arrange(desc(ratio)) %>% 
  head(5)

# 컬럼의 이름을 변경
df = rename(midwest, asian = popasian, total = poptotal)
# 특정 컬럼을 선택
df2 = df[, c('county', 'asian', 'total')]
# 새로운 컬럼을 생성
ratio = df2$asian / df2$total * 100
df2$ratio = ratio
# 내림차순 정렬 
flag = order(-df2$ratio)
df3 = df2[flag, ]
head(df3, 5)

# ratio컬럼 데이터에서 전체 평균 데이터보다 크다면 'large'
# 같다면 'middle'
# 작다면 'small' 데이터를 가지는 새로운 파생변수(group) 생성

# ratio 컬럼의 평균을 저장 
mean(df3$ratio) -> mean_value
# ifelse(조건식 : ratio 데이터값 > 평균값 , 결과.... )
ifelse(
  df3$ratio > mean_value, 
  'large', 
  ifelse(
    df3$ratio == mean_value, 
    'middle', 
    'small'
  )
) -> group_data
# 새로운 컬럼에 대입 
df3$group = group_data

midwest %>% 
  rename(asian = popasian, total = poptotal) %>% 
  select(county, total, asian) %>% 
  mutate(ratio = (asian / total)*100 ) %>% 
  arrange(desc(ratio)) %>% 
  mutate(group = 
           ifelse(
             ratio > mean(ratio), 
             'large', 
             ifelse(
               ratio == mean(ratio), 
               'middle', 
               'small'
             )
           ))

table(df3$group)
# table 함수의 기능을 반복문으로 확인 
df3$group
large_cnt = 0
middle_cnt = 0
small_cnt = 0
for (i in df3$group){
    # 만약에 i가 large 라면?
  if(i == 'large'){
    # large_cnt를 1 증가시킨다. 
    large_cnt = large_cnt + 1
  }else if(i == 'middle'){
    middle_cnt = middle_cnt + 1
  }else{
    small_cnt = small_cnt + 1
  }
}
print(large_cnt)
print(middle_cnt)
print(small_cnt)
