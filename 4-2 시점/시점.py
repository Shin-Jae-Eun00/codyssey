import pandas as pd
import matplotlib.pyplot as plt

# 1. CSV 파일 불러오기
df_gender = pd.read_csv('시점_남여.csv', encoding='cp949')
df_age = pd.read_csv('시점_연령별인구.csv', encoding='cp949')

# 2. 컬럼 공백 제거
df_gender.columns = df_gender.columns.str.strip()
df_age.columns = df_age.columns.str.strip()

# 3. 시점 숫자 변환 (문자 제거eh...)
df_gender = df_gender[pd.to_numeric(df_gender['시점'], errors='coerce').notnull()]
df_gender['시점'] = df_gender['시점'].astype(int)

df_age = df_age[pd.to_numeric(df_age['시점'], errors='coerce').notnull()]
df_age['시점'] = df_age['시점'].astype(int)

# 4. 2015년 이후 데이터 필터링
df_gender = df_gender[df_gender['시점'] >= 2015]
df_age = df_age[df_age['시점'] >= 2015]

# -----------------------------
# 성별 데이터 변환
# -----------------------------
df_gender_long = pd.melt(
    df_gender,
    id_vars='시점',
    value_vars=['남자', '여자'],
    var_name='성별',
    value_name='일반가구원'
)

# 일반가구원만 남기고
df_gender_final = df_gender_long[['시점', '성별', '일반가구원']]

# -----------------------------
# 남녀 연도별 통계
# -----------------------------
gender_result = df_gender_final.pivot(
    index='시점',
    columns='성별',
    values='일반가구원'
)

print("\n📊 남자 / 여자 연도별 일반가구원")
print(gender_result)

# -----------------------------
# 연령별 일반가구원 데이터
# -----------------------------
print("\n📊 연령별 일반가구원")
print(df_age)

# -----------------------------
# 그래프
# -----------------------------
plt.figure(figsize=(14, 5))

# ▶ 남녀 그래프
plt.subplot(1, 2, 1)

plt.plot(gender_result.index, gender_result['남자'], marker='o', linewidth=2, label='남자')
plt.plot(gender_result.index, gender_result['여자'], marker='o', linewidth=2, label='여자')

plt.title('population by Gender (2015~)')
plt.xlabel('Year')
plt.ylabel('population')

plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(gender_result.index, rotation=45)
plt.legend()

# 연령별 그래프
plt.subplot(1, 2, 2)

for col in df_age.columns:
    if col != '시점':
        plt.plot(df_age['시점'], df_age[col], marker='s', linewidth=1.5, label=col)

plt.title('population by Age Group')
plt.xlabel('Year')
plt.ylabel('population')

plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(df_age['시점'], rotation=45)

# 범례 밖으로 + 글자 작게
plt.legend(
    bbox_to_anchor=(1.05, 1),
    loc='upper left',
    fontsize=8,
    ncol=1
)

plt.tight_layout()

# 전체
plt.tight_layout()
plt.show()
