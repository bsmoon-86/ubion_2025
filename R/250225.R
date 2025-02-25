library(dplyr)
library(ggplot2)

midwest = ggplot2::midwest


# 미성년자의 인구 비율이 낮은 하위 5개의 지역을 출력
# popadults 컬럼의 이름을 adult 변경(rename)
# poptotal 컬럼의 이름을 total 변경(rename)
# child 컬럼을 생성 -> total - adult(mutate)
# child_ratio 컬럼을 생성 -> (child / total) * 100 (mutate)
# child_ratio 컬럼을 기준으로 오름차순 정렬(arrange)
# 상위 5개를 출력(head)
midwest %>% 
  rename(adult = popadults) %>% 
  rename(total = poptotal) %>% 
  mutate(child = total - adult) %>% 
  mutate(child_ratio = (child / total) * 100) %>% 
  arrange(child_ratio) %>% 
  select(county ,adult, total, child, child_ratio) %>% 
  tail(5) -> df
df

# ifelse()함수를 간단하게 구현 
# 조건식이 참인경우 출력은 2번째 인자 값
# 조건식이 거짓인 경우 출력은 3번째 인자 값
# 1번째 인자는 조건식
iftest = function(flag, t_value, f_value){
  # 결과 값을 데이터의 타입은 벡터
  result = c()
  # 위치 변수를 하나 생성 
  result_index = 1
  # flag -> c(TRUE, FALSE, FALSE)
  # flag데이터를 반복문을 생성하여 하나씩 비교
  for (i in flag){
    if (i){
      # result라는 변수 result_index 위치에 t_value 대입
      result[result_index] = t_value
    }else{
      # result라는 변수 result_index 위치에 f_value 대입
      result[result_index] = f_value
    }
    # index의 값을 1 증가시킨다. 
    result_index = result_index + 1
  }
  # result를 되돌려준다. 
  return (result)
}

flag_test = c(TRUE, FALSE, FALSE)
iftest(flag_test, 'T', 'F')

iftest( df$child_ratio > 49 , 'large', 'small' ) -> df$test
df


# 시각화
mpg = ggplot2::mpg
View(mpg)

# 산점도 그래프 
ggplot(
  data=mpg, 
  aes(x= displ, y=hwy)
       ) + geom_point()
# 막대 그래프 
ggplot(
  data=mpg, 
  aes(x = drv)
) + geom_bar()
table(mpg$drv)

mpg %>% 
  group_by(drv) %>% 
  summarise(mean_hwy = mean(hwy)) -> group_data

ggplot(
  data = group_data, 
  aes(x = drv, y = mean_hwy)
) + geom_col()

# 박스플롯
ggplot(
  data = mpg, 
  aes(x = drv, y = hwy)
) + geom_boxplot()

# 라인 그래프 
group_data2 = mpg %>% 
  group_by(year) %>% 
  summarise(count = n())
group_data2

ggplot(
  data = group_data2, 
  aes(x = year, y = count)
) + geom_line()

# 외부 데이터 로드 
# .sav 확장자 파일 로드 
install.packages('foreign')
library(foreign)

read.spss("./data/Koweps.sav", to.data.frame = T) -> welfare

# 데이터프레임중 특정 컬럼만 추출하고 컬럼의 이름을 변경 
df = welfare %>% 
  rename(
    gender = h10_g3, 
    birth = h10_g4, 
    code_job = h10_eco9, 
    income = p1002_8aq1, 
    loc = h10_reg7
  ) %>% 
  select(gender, birth, code_job, income, loc)
head(df)

# 결측치
NA + 10
10+NA
NA == NA
NA != NA
# 데이터프레임에서 정보 출력 
str(df)
summary(df)

table(is.na(df))

# 컬럼별로 결측치의 개수 출력 
table(is.na(df$gender))
table(is.na(df$birth))
table(is.na(df$code_job))
table(is.na(df$income))
table(is.na(df$loc))

# 데이터 수정 
# 성별 데이터를 1은 male 2는 female 변경
table(df$gender)

df$gender
ifelse(
  # 조건식
  df$gender == 1, 
  'male', 
  ifelse(
    df$gender == 2, 
    'female', 
    NA
  )
) -> df$gender
table(df$gender)
table(is.na(df$gender))

# 과연 성별 평균 임금의 차이가 얼마나 나는가?
# 특정 컬럼을 선택 -> gender, income  (select)
# income 컬럼에서 0과 결측치를 제외시킨다. (filter)
# gender를 기준으로 그룹화 (group_by)
# 그룹화 연산 income의 평균 값 (summaries)
# 변수에 저장 
# 막대그래프 시각화해서 표시

df %>% 
  select(gender, income) %>% 
  # 인덱스의 조건식 : 0이 아닌 경우, 9999가 아닌 경우 
  # ,결측치 아닌경우
  # filter(!is.na(income)) %>% 
  # filter(income != 0) %>% 
  # filter(income != 9999)
  filter(!is.na(income) & income != 0 & income != 9999) %>% 
  group_by(gender) %>% 
  summarise(gender_mean = mean(income)) -> gender_income

ggplot(
  data = gender_income, 
  aes(x = gender, y = gender_mean)
) + geom_col()

# 나이에 따른 평균 임금의 차이가 어떻게 되는가?
# 나이라는 컬럼이 존재하지 않는다. 
# age 컬럼을 생성 -> 현재년도(2015) - 태어난 년도(birth)
# income 컬럼의 데이터에서 결측치와 0, 9999인 데이터를 제거 
# 나이를 기준으로 그룹화 
# 그룹화 연산 : income 평균 값
# 변수(age_income)에 저장 
# 가장 평균 임금이 높은 5개의 데이터를 확인 
# age_income 데이터를 막대 그래프 시각화

df %>% 
  mutate(age = 2015 - birth) %>%
  filter(!is.na(income) & !income %in% c(0, 9999)) %>% 
  group_by(age) %>% 
  summarise(income_mean = mean(income)) -> age_income
  
age_income %>% 
  arrange(desc(income_mean)) %>% 
  head(5)

ggplot(
  data = age_income, 
  aes(x = age, y = income_mean)
) + geom_col()

# 연령대별 평균 임금 
# income의 결측치와 0, 9999를 포함한 값들은 제거 
# 나이 컬럼을 생성 
# 연령대 컬럼을 생성 
# (40세 미만 - 'young', 
# 40세 이상 60세 미만 - 'middle'
# 60세 이상 - 'old')
# 연령대 컬럼을 기준으로 그룹화
# 그룹화 연산 - income 평균 
# 변수 저장
# 막대 그래프 시각화 
df %>% 
  filter(!is.na(income) & !income %in% c(0,9999)) %>% 
  mutate(
    age = 2015 - birth, 
    ageg = ifelse(
      age < 40, 
      'young', 
      ifelse(
        age < 60, 
        'middle', 
        'old'
      )
    )
  ) %>% 
  group_by(ageg) %>% 
  summarise(income_mean = mean(income)) -> ageg_income

ggplot(
  data = ageg_income, 
  aes(x = ageg, y = income_mean)
) + geom_col() + scale_x_discrete(
  limits = c('young', 'middle', 'old')
)

# 지역별 평균 임금을 확인 
# income 데이터에서 결측치, 0, 9999는 제외
# 그룹화 지역을 기준으로 
# 연산은 income의 평균
# 지역별 평균 임금을 출력 
df %>% 
  filter(!is.na(income) & !income %in% c(0,9999)) %>% 
  group_by(loc) %>% 
  summarise(income_mean = mean(income))

# 지역별 남녀 평균 임금을 확인 
# income 데이터에서 결측치, 0, 9999는 제외
# 그룹화 지역, 성별을 기준으로 
# 연산은 income의 평균
# 지역, 성별 평균 임금을 출력 
# 그래프 시각화
df %>% 
  filter(!is.na(income) & !income %in% c(0,9999)) %>% 
  group_by(loc, gender) %>% 
  summarise(income_mean = mean(income)) -> loc_gender_income

ggplot(
  data = loc_gender_income, 
  aes(x = loc, y = income_mean, fill=gender)
  ) + geom_col(
    position = 'dodge'
  ) -> loc_gender_col
# 인터렉티브 그래프를 위한 패키지
install.packages('plotly')
library(plotly)
ggplotly(loc_gender_col)

# 엑셀 파일을 로드 
# 패키지 설치 
install.packages('readxl')
library(readxl)

read_excel('./data/Koweps_Codebook.xlsx', 
           sheet = 2) -> code_book

head(df, 1)

# left_join  조건 컬럼 code_job
left_join(
  df, code_book, by='code_job'
) -> total_df

# total_df데이터에서 code_job데이터가 결측치가 아니고
# job이 결측치인 데이터가 존재하는가?
total_df %>% 
  filter(!is.na(code_job)) %>% 
  filter(is.na(job))

# 과연 평균 임금이 가장 높은 상위의 직업 10개는 무엇인가?
total_df %>% 
  filter(!is.na(job)) %>% 
  filter(!is.na(income) & !income %in% c(0,9999)) %>% 
  group_by(job) %>% 
  summarise(
    income_mean = mean(income), 
    cnt = n()) %>% 
  filter(cnt >= 10) %>% 
  arrange(-income_mean) -> job_income

ggplot(
  data = head(job_income, 10), 
  aes(x = reorder(job, income_mean), 
      y = income_mean)
)+ geom_col() + coord_flip()


# 남자의 기준으로 평균 임금이 높은 상위 10개의 직업
total_df %>% 
  filter(gender == 'male') %>% 
  filter(!is.na(job)) %>% 
  filter(!is.na(income) & !income %in% c(0, 9999)) %>% 
  group_by(job) %>% 
  summarise(income_mean = mean(income), 
            cnt = n()) %>% 
  filter(cnt >= 10) %>% 
  arrange(desc(income_mean)) %>% 
  head(10) -> male_data



# 여자의 기준으로 평균 임금이 높은 상위 10개의 직업 
# job의 결측치를 제거 
# income의 결측치, 0, 9999를 제외
# gender, job을 기준으로 그룹화
# 그룹화 연산 :income의 평균, 개수
# gender가 female인 데이터만 추출
# cnt 가 10 이상인 데이터만 추출
# 평균 임금의 내림차순 정렬 
# 상위 10개만 출력
total_df %>% 
  filter(!is.na(job)) %>% 
  filter(!is.na(income) & !income %in% c(0, 9999)) %>% 
  group_by(gender, job) %>% 
  summarise(income_mean = mean(income), 
            cnt = n()) %>% 
  filter(gender == 'female') %>% 
  filter(cnt >= 10) %>% 
  arrange(desc(income_mean)) %>% 
  head(10) -> female_data

rbind(male_data, female_data)
bind_rows(male_data, female_data) -> total_data
# total_data에 있는 gender 부분의 결측치에 'male'대체
ifelse(
  total_data$gender != 'female', 
  'male', 
  total_data$gender
)
ifelse(
  is.na(total_data$gender), 
  'male', 
  total_data$gender
) -> total_data$gender
total_data

