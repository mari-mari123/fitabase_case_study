# Introduction
## Analysis overview
## Project information
## About the company
## Analysis and Business object

## envirenment
Tip: Apple M1
OS: version 15.0
python: 3.13.2
pip: 25.0



Chief Creative Officer(Urška Sršen) has asked the marketing analytics team to focus on a Bellabeat product and analyze smart device usage data in order to gain insight into how people are already using their smart devices.

## 自分用のメモ
pandasを使うのにあたって今回仮想環境を使うことにした。
理由はプロジェクトごとに依存関係を気にするのが難しそうだと思ったので。
Step1: myenvという仮想環境をpython内に作成
python3 -m venv myenv
Step2:仮想環境をアクティブ化
source myenv/bin/activate
Step3: 仮想環境内でpandasをインストール
pip install pandas
Step4: プロジェクトがおわったら仮想環境を無効化 ←このプロジェクトがおわったら必ずやってね
deactivate

# Ask
1.1 Task
* Identify the business task
* Consider key stakeholders

1.2 Business Tasks
Our team's tasks are to identify the trends of the usage of smart devices (non-Bellabeat smart devices) and find how customers use non-Bellabeat devices. Also, we will give recommendations for Bellabeat marketing strategy.


1.3 key stakeholders

* Urška Sršen: Bellabeat’s co founder and Chief Creative Officer
* Sando Mur: Mathematician and Bellabeat cofounder; key member of the Bellabeat executive team
* Bellabeat marketing analytics team: A team of data analysts responsible for collecting, analyzing, and reporting data that helps guide Bellabeat’s marketing strategy.


# Prepare
2.1 Task
* Download data and store it appropriately.
* Identify how it’s organized.
* Sort and filter the data.
* Determine the credibility of the data.

2.2 the place where the data are stored
* They are stored in local
file path for the data from March 12th to April 11th: Documents/Data Analyst/fitabaseData/mturkfitbit_export_3.12.16-4.11.16
file path for the data from April 12th to May 12th: Documents/Data Analyst/fitabaseData/mturkfitbit_export_4.12.16-5.12.16

2.3 how the data is organized
* 'dailyActivity_merged.csv' are long format
* Each row has the record of one day's activity divided by Id.

2.4 Sort and filter the data
* Marge two separate file ('Fitabase Data 3.12.16-4.11.16/dailyActivity_merged.csv' and 'Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv')
``` python
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
```

* Identify and fix duplicate data
``` python
duplicates = df_combine[df_combine.duplicated(subset=['Id', 'ActivityDate'], keep=False)]
print(duplicates)

# the data disapeared because of grouping
df_combine['ActivityDate'] = pd.to_datetime(df_combine['ActivityDate'], format='%m/%d/%Y')

# get a mean
df_grouped = df_combine.groupby(['Id', 'ActivityDate']).mean().reset_index()
duplicates_grouped = df_grouped[df_grouped.duplicated(subset=['Id', 'ActivityDate'], keep=False)]

if duplicates_grouped.empty:
  print("there is no duplicates")
else:
  print(duplicates_grouped)

# check whether the not needed data is not delited
duplicates_count = df_combine.duplicated(subset=['Id', 'ActivityDate'], keep=False).sum()
print(duplicates_count) #-> 48
print(df_grouped.tail()) #1396-24=1372 only duplicated data were fixed
```

* checking for missing values
``` python
print(df_grouped.isnull().sum())
```

``` python
# the result -> nothing
Id                          0
ActivityDate                0
TotalSteps                  0
TotalDistance               0
TrackerDistance             0
LoggedActivitiesDistance    0
VeryActiveDistance          0
ModeratelyActiveDistance    0
LightActiveDistance         0
SedentaryActiveDistance     0
VeryActiveMinutes           0
FairlyActiveMinutes         0
LightlyActiveMinutes        0
SedentaryMinutes            0
Calories                    0
```

2.5 Determine the credibility of the data
ROCCC
| ROCCC            | Result      |
|:-----------------|------------:|
| Reliable         | This dataset is not fully reliable because the data description states that thirty eligible Fitbit users consented, yet the dataset contains data from 33 to 35 individuals.|
| Origin           | This dataset was made by Furberg, Brinton, Keting, Keating and Ortiz. Its origin is Zendo.org.|
| Comprehensive    | Not clear because there is no information in sex, age and how to correct data.|
| Current         | No. This dataset is made based on 2016. That's why this dataset is not the latest information. The data was last refreshed on March 31th, 2016.|
| Cited            | Yes. There is a citation. |

* checking data type
``` python
print(df.grouped.dtypes)
```
``` python
# the result -> OK
Id                                   int64
ActivityDate                datetime64[ns]
TotalSteps                         float64
TotalDistance                      float64
TrackerDistance                    float64
LoggedActivitiesDistance           float64
VeryActiveDistance                 float64
ModeratelyActiveDistance           float64
LightActiveDistance                float64
SedentaryActiveDistance            float64
VeryActiveMinutes                  float64
FairlyActiveMinutes                float64
LightlyActiveMinutes               float64
SedentaryMinutes                   float64
Calories                           float64
```
* range validation
```python
#  checking values more than or equal to 0
for column in df_grouped.columns[2:]:
  print('Checking:', column)
  result = df_grouped[df_grouped[column] < 0]

  if not result.empty:
    print('Found negativi values in', column)
    print(result[[column]])
  else:
    print('No negative values in', column)
```
``` python
# result -> OK
Checking: TotalSteps
No negative values in TotalSteps
Checking: TotalDistance
No negative values in TotalDistance
Checking: TrackerDistance
No negative values in TrackerDistance
Checking: LoggedActivitiesDistance
No negative values in LoggedActivitiesDistance
Checking: VeryActiveDistance
No negative values in VeryActiveDistance
Checking: ModeratelyActiveDistance
No negative values in ModeratelyActiveDistance
Checking: LightActiveDistance
No negative values in LightActiveDistance
Checking: SedentaryActiveDistance
No negative values in SedentaryActiveDistance
Checking: VeryActiveMinutes
No negative values in VeryActiveMinutes
Checking: FairlyActiveMinutes
No negative values in FairlyActiveMinutes
Checking: LightlyActiveMinutes
No negative values in LightlyActiveMinutes
Checking: SedentaryMinutes
No negative values in SedentaryMinutes
Checking: Calories
No negative values in Calories
```

* Consistency check
To find values when TotalSteps are 0, Calories are not 0.
Such a data is 127 rows.
```python
inconsistent_data = df_grouped[(df_grouped['TotalSteps'] == 0) & (df_grouped['Calories'] != 0)]

if not inconsistent_data.empty:
  for column in df_grouped.columns[3:-1]:
    print('Checking: ',column)
    column_inconsistent = inconsistent_data[inconsistent_data[column] != 0]
    print(column_inconsistent)
else:
  print('NO data found')
```

So we have to check whether it was recorded any activities, except for TotalSteps for 127 rows.

- There is calorie consumption but no activity record → Exclude
```python
non_zero_calories = df_grouped[(df_grouped['Calories'] != 0) & (df_grouped.iloc[:, :-1].eq(0).all(axis=1))]
print(non_zero_calories)
```
- There is no calorie consumption but an activity record exists → Exclude
```python
zero_calories = df_grouped[(df_grouped['Calories'] == 0) & (df_grouped.iloc[:, :-1].ne(0).all(axis=1))]
print(zero_calories)
```
- Check if the consumed calories are abnormally high (more than 10,000) → Exclude
```python
unrealistic_calories = df_grouped[df_grouped['Calories'] > 10000]
print(unrealistic_calories)
```
- Check if the step count is extremely high (more than 100,000) → Exclude
```python
unrealistic_steps = df_grouped[df_grouped['TotalSteps'] > 100000]
print(unrealistic_steps)
```
- TotalDistance = TrackerDistance + LoggedActivitiesDistance?
```python
df_grouped['TotalDistance'] = round(df_grouped['TotalDistance'],2)
df_grouped['calculated_total_distance'] = round(df_grouped['TrackerDistance'] + df_grouped['LoggedActivitiesDistance'],2)
print(df_grouped[['calculated_total_distance', 'TotalDistance']].head())

# Rows where TotalDistance does not match calculated_total_distance → Column 54
# Possible device synchronization errors or missing data, so modify TotalDistance to match calculated_total_distance

not_equal_total_distance = df_grouped[df_grouped['calculated_total_distance'] != df_grouped['TotalDistance']]
print(not_equal_total_distance)
df_grouped['TotalDistance'] = df_grouped['calculated_total_distance']
```

- Ensure no future dates are included → OK
```python
future_dates = df_grouped[df_grouped['ActivityDate'] > pd.to_datetime('today')]
print(future_dates)
```
- Ensure there are no duplicate combinations of ID and ActivityDate → OK
```python
duplicate_id_date = df_grouped[df_grouped.duplicated(subset=['Id', 'ActivityDate'], keep=False)]
if duplicate_id_date.empty:
  print('There is no duplicates')
else:
  print(duplicate_id_date)
```

# Process
データのスクリーニングまたは操作の文書化
3.1 Task
1. Check the data for errors.
2. Choose your tools.
3. Transform the data so you can work with it effectively.
4. Document the cleaning process.


# Analyze
分析の要約

# Share
補足的な視覚化と主な発見

# Act
分析に基づく、上位レベルのコンテンツ推奨事項
