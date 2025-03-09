# 3.1 Task
# 1. Check the data for errors.
'''
I have already checked the following during the prepare phase:
* check for missing value -> None
* check for date type
* Check for duplicates -> There are duplicates with the same date and same Id, but different values.
'''

# 2. Choose your tools.
'''
I choose Python because:
* it is easier to manupulate data.
* I am not affected by limitations such as data size constraints.
'''

# 3. Transform the data so you can work with it effectively.

# I will make a new file to get clean data file
import pandas as pd
import datetime as dt

# data from March to April
df_daily_april = pd.read_csv('mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/dailyActivity_merged.csv')

# data from April to May
df_daily_may = pd.read_csv('mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv')

# combine two file
df_combine = pd.concat([df_daily_april, df_daily_may], ignore_index=True)

'''
check duplicate -> there are duplicates. they are same date and same Id, but the other values are different. I am not sure why this happens, so I decided to take the mean of both values, assuming they might carry some significance.
'''
duplicates = df_combine[df_combine.duplicated(subset=['Id', 'ActivityDate'], keep=False)]

#while combining two datasets, some data disappeared because both date format are different.
df_combine['ActivityDate'] = pd.to_datetime(df_combine['ActivityDate'], format='%m/%d/%Y')

# get a mean
df_grouped = df_combine.groupby(['Id', 'ActivityDate']).mean().reset_index()
duplicates_grouped = df_grouped[df_grouped.duplicated(subset=['Id', 'ActivityDate'], keep=False)]

# TotalDistance = TrackerDistance + LoggedActivitiesDistance?
df_grouped['TotalDistance'] = round(df_grouped['TotalDistance'],2)
df_grouped['CalculatedTotalDistance'] = round(df_grouped['TrackerDistance'] + df_grouped['LoggedActivitiesDistance'],2)

'''
There are some rows such that TotalDIstanceとCalculatedTotalDistance are different ->54 rows
I assume that it happens because of missing of connecting device or missing data
That's why I modify from TotalDistance to CalculatedTotalDistance.
'''
not_equal_total_distance = df_grouped[df_grouped['CalculatedTotalDistance'] != df_grouped['TotalDistance']]
df_grouped['TotalDistance'] = df_grouped['CalculatedTotalDistance']

# Delete a column 'TotalDistance'
'''
- The original `TotalDistance` column contained incorrect values that did not match `TrackerDistance + LoggedActivitiesDistance`.
- We assumed that `CalculatedTotalDistance = TrackerDistance + LoggedActivitiesDistance` is the correct total distance.
- Therefore, `TotalDistance` was removed and replaced with `CalculatedTotalDistance`.
'''
column_without_TotalDistance = [
  'Id', 'ActivityDate', 'TotalSteps', 'TrackerDistance', 'LoggedActivitiesDistance', 'VeryActiveDistance', 'ModeratelyActiveDistance', 'LightActiveDistance',
  'SedentaryActiveDistance', 'VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes', 'Calories', 'CalculatedTotalDistance'
  ]
df_grouped_without_TotalDistance = df_grouped[column_without_TotalDistance]

'''
I have already checked in Prepare phase below, so I don't do here:
* Check whether the columns in both files are the same
* check duplicate
* confirm whether the number of rows were changed while combining two datasets
'''

# To make a new dataset
df_grouped_without_TotalDistance.to_csv('daily_activity_data.csv', index = False)



# -----------------------------------------------------
#set dataframe with our new csv dataset
df_daily = pd.read_csv('daily_activity_data.csv')

# check unique user
print(f"daily_activity_data: {df_daily.Id.nunique()} unique users")

# Assign columns except for 'ActivityDate'
column_without_date = [
  'Id', 'TotalSteps', 'TrackerDistance', 'LoggedActivitiesDistance', 'VeryActiveDistance', 'ModeratelyActiveDistance', 'LightActiveDistance', 'SedentaryActiveDistance', 'VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes', 'Calories', 'CalculatedTotalDistance'
  ]

# overview of whole data
summary = df_daily.describe()
print(summary)

# sum and mean by Id
df_by_Id_sum = round(df_daily[column_without_date].groupby('Id').sum(), 2)
df_by_Id_mean = round(df_daily[column_without_date].groupby('Id').mean(), 2)
print(df_by_Id_sum)
print(df_by_Id_mean)

# --------------------------------------------------------------
# add weekday column
print(df_daily.dtypes)
# The datetype of ActivityDate became object, so I changed the datatype from object to datetime64[ns]
df_daily['ActivityDate'] = pd.to_datetime(df_daily['ActivityDate'])

df_daily['WeekDay'] = df_daily['ActivityDate'].dt.day_name()
print(df_daily)

# 4. Document the cleaning process.
'''
すでに Process の中で修正の理由を書いているので、最後に 「全体をまとめた一連のクリーニング手順」 を簡潔に整理するといいと思う。
何を、なぜ、どのように修正したか を時系列順に書くと、あとで見直したときに理解しやすくなるよ！
'''
