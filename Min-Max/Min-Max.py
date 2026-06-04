import random
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

# 데이터 읽기
column_names = [
    'Sex',
    'Length',
    'Diameter',
    'Height',
    'Whole weight',
    'Shucked weight',
    'Viscera weight',
    'Shell weight',
    'Rings'
]

df = pd.read_csv(
    'abalone.txt',
    header=None,
    names=column_names
)

print('원본 데이터')
print(df.head())

# 성별 컬럼 분리
label = df['Sex']
data = df.drop('Sex', axis=1)

print('\n성별 분포')
print(label.value_counts())

# Min-Max Scaling 직접 구현
manual_minmax = data.copy()

for column in manual_minmax.columns:

    min_value = manual_minmax[column].min()
    max_value = manual_minmax[column].max()

    manual_minmax[column] = (
        (manual_minmax[column] - min_value)
        / (max_value - min_value)
    )

print('\n직접 구현 Min-Max Scaling')
print(manual_minmax.head())

# sklearn Min-Max Scaling
minmax_scaler = MinMaxScaler()

minmax_data = minmax_scaler.fit_transform(data)

minmax_df = pd.DataFrame(
    minmax_data,
    columns=data.columns
)

print('\nsklearn Min-Max Scaling')
print(minmax_df.head())


# Standard Scaling 직접 구현
manual_standard = data.copy()

for column in manual_standard.columns:

    mean_value = manual_standard[column].mean()
    std_value = manual_standard[column].std()

    manual_standard[column] = (
        (manual_standard[column] - mean_value)
        / std_value
    )

print('\n직접 구현 Standard Scaling')
print(manual_standard.head())

# sklearn Standard Scaling
standard_scaler = StandardScaler()

standard_data = standard_scaler.fit_transform(data)

standard_df = pd.DataFrame(
    standard_data,
    columns=data.columns
)

print('\nsklearn Standard Scaling')
print(standard_df.head())

# Random Over Sampling
counts = label.value_counts()

max_count = counts.max()

over_data = data.copy()
over_label = label.copy()

for class_name in counts.index:

    class_data = data[label == class_name]

    diff = max_count - len(class_data)

    if diff > 0:

        sampled_index = random.choices(
            class_data.index.tolist(),
            k=diff
        )

        new_data = data.loc[sampled_index]
        new_label = label.loc[sampled_index]

        over_data = pd.concat(
            [over_data, new_data],
            ignore_index=True
        )

        over_label = pd.concat(
            [over_label, new_label],
            ignore_index=True
        )

print('\nRandom Over Sampling 결과')
print(over_label.value_counts())

# Random Under Sampling
counts = label.value_counts()

min_count = counts.min()

under_data_list = []
under_label_list = []

for class_name in counts.index:

    class_data = data[label == class_name]

    sampled_index = random.sample(
        class_data.index.tolist(),
        min_count
    )

    under_data_list.append(
        data.loc[sampled_index]
    )

    under_label_list.append(
        label.loc[sampled_index]
    )

under_data = pd.concat(
    under_data_list,
    ignore_index=True
)

under_label = pd.concat(
    under_label_list,
    ignore_index=True
)

print('\nRandom Under Sampling 결과')
print(under_label.value_counts())