# --- 2.4 sort and filter the data
import pandas as pd

# data from March to April
df_daily_april = pd.read_csv('mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/dailyActivity_merged.csv')

# data from April to May
df_daily_may = pd.read_csv('mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv')

# check only above 5 data
print(df_daily_april.head())
print(df_daily_may.head())

# check whether the columns in the both files are the same -> they are the same column

column1 = df_daily_april.columns
column2 = df_daily_may.columns

if column1.equals(column2):
  print("they are same column")
else:
  print("the column name are different")
  print("file 1 column name:", column1)
  print("file 2 column name:", column2)

# combine two file
df_combine = pd.concat([df_daily_april, df_daily_may], ignore_index=True)
print(df_combine.head())
print(df_combine.tail())

# check duplicate ->重複データがあり。同じ日付、同じIDだが数値が異なる。原因がわからないため平均値を取ることにする。全く同じ数値ではないので数値には何らかの意味があるため。
duplicates = df_combine[df_combine.duplicated(subset=['Id', 'ActivityDate'], keep=False)]
print(duplicates)

#グループ化するときに一部のデータが消えてしまったので
df_combine['ActivityDate'] = pd.to_datetime(df_combine['ActivityDate'], format='%m/%d/%Y')

# get a mean
df_grouped = df_combine.groupby(['Id', 'ActivityDate']).mean().reset_index()
duplicates_grouped = df_grouped[df_grouped.duplicated(subset=['Id', 'ActivityDate'], keep=False)]
# データフレームが空かどうか調べるにはemptyを使う。
if duplicates_grouped.empty:
  print("there is no duplicates")
else:
  print(duplicates_grouped)

# グループ化前後でrowの数に間違いがないかを確認
duplicates_count = df_combine.duplicated(subset=['Id', 'ActivityDate'], keep=False).sum()
print(duplicates_count)
print(df_grouped.tail()) #1396-24=1372 重複分のみ消えてるからOK

# checking for missing values
print(df_grouped.isnull().sum())


# ---2.5 Determine the credibility of the data
# Data integrity verification
# 1. Checking the data type
print(df_grouped.dtypes)

# 2. Range validation -> Nothing
for column in df_grouped.columns[2:]:
  print('Checking:', column)
  result = df_grouped[df_grouped[column] < 0]

  if not result.empty:
    print('Found negativi values in', column)
    print(result[[column]])
  else:
    print('No negative values in', column)

inconsistent_data = df_grouped[(df_grouped['TotalSteps'] == 0) & (df_grouped['Calories'] != 0)]

if not inconsistent_data.empty:
  for column in df_grouped.columns[3:-1]:
    print('Checking: ',column)
    column_inconsistent = inconsistent_data[inconsistent_data[column] != 0]
    print(column_inconsistent)
else:
  print('NO data found')


# カロリー消費があるのに行動記録がなにもない->なし
non_zero_calories = df_grouped[(df_grouped['Calories'] != 0) & (df_grouped.iloc[:, :-1].eq(0).all(axis=1))]
print(non_zero_calories)
# カロリー消費がないのに行動記録がある->なし
zero_calories = df_grouped[(df_grouped['Calories'] == 0) & (df_grouped.iloc[:, :-1].ne(0).all(axis=1))]
print(zero_calories)

# 消費カロリーが以上に高すぎないか(more than 10000)->なし
unrealistic_calories = df_grouped[df_grouped['Calories'] > 10000]
print(unrealistic_calories)

# 歩数が非常に高いか
unrealistic_steps = df_grouped[df_grouped['TotalSteps'] > 100000]
print(unrealistic_steps)

# TotalDistance = TrackerDistance + LoggedActivitiesDistance?
df_grouped['TotalDistance'] = round(df_grouped['TotalDistance'],2)
df_grouped['calculated_total_distance'] = round(df_grouped['TrackerDistance'] + df_grouped['LoggedActivitiesDistance'],2)
print(df_grouped[['calculated_total_distance', 'TotalDistance']].head())

# TotalDIstanceとcalculated_total_distanceが一致していない行->54列
# デバイスの同期ミスやデータの欠損の可能性があるのでTotalDIstanceをcalculated_total_distanceへ修正
not_equal_total_distance = df_grouped[df_grouped['calculated_total_distance'] != df_grouped['TotalDistance']]
print(not_equal_total_distance)
df_grouped['TotalDistance'] = df_grouped['calculated_total_distance']


# 日付の整合性：未来の日付が含まれていないか ->OK
future_dates = df_grouped[df_grouped['ActivityDate'] > pd.to_datetime('today')]
print(future_dates)

# IDとActivityDateが重複している組み合わせが無いか？->OK
duplicate_id_date = df_grouped[df_grouped.duplicated(subset=['Id', 'ActivityDate'], keep=False)]
if duplicate_id_date.empty:
  print('There is no duplicates')
else:
  print(duplicate_id_date)
