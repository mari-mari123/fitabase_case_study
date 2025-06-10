# 1. Check the data for errors.
'''
I have already checked the following during the prepare phase:
* Check for missing values -> None
* Check for date types
* Check for duplicates -> There are duplicates with the same date and same Id, but different values.
'''

# 2. Choose your tools.
'''
I chose Python because:
* It is easier to manipulate data.
* I am not affected by limitations such as data size constraints.
'''

# 3. Transform the data so you can work with it effectively.

# I will make a new file to get clean data file
import pandas as pd
import datetime as dt

# data from March to April
df_daily_april = pd.read_csv('data/raw_data/mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/dailyActivity_merged.csv')

# data from April to May
df_daily_may = pd.read_csv('data/raw_data/mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv')

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
df_grouped_without_TotalDistance.to_csv('data/daily_activity_data.csv', index = False)

# -----------------------------------------------------
#set dataframe with our new csv dataset
df_daily = pd.read_csv('data/daily_activity_data.csv')

# check unique user
print('------------Unique_user-----------')
print(f"daily_activity_data: {df_daily.Id.nunique()} unique users")

# Assign columns except for 'ActivityDate'
column_without_date = [
  'Id', 'TotalSteps', 'TrackerDistance', 'LoggedActivitiesDistance', 'VeryActiveDistance', 'ModeratelyActiveDistance', 'LightActiveDistance', 'SedentaryActiveDistance', 'VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes', 'Calories', 'CalculatedTotalDistance'
  ]

# overview of whole data
summary = df_daily.describe()
print('------------Summary-----------')
print(summary)

# sum and mean by Id
df_by_Id_sum = round(df_daily[column_without_date].groupby('Id').sum(), 2)
df_by_Id_mean = round(df_daily[column_without_date].groupby('Id').mean(), 2)
print('------------Sum by Id-----------')
print(df_by_Id_sum)
print('------------Mean by Id-----------')
print(df_by_Id_mean)

# --------------------------------------------------------------
# add weekday column
print(df_daily.dtypes)
# The datetype of ActivityDate became object, so I changed the datatype from object to datetime64[ns]
df_daily['ActivityDate'] = pd.to_datetime(df_daily['ActivityDate'])

df_daily['WeekDay'] = df_daily['ActivityDate'].dt.day_name()
print(df_daily)

# update csv file to add weekday column
df_daily.to_csv('ddata/daily_activity_data_analyze.csv', index = False)

# 4. Document the cleaning process.
'''
* Step 1: Check the data for errors
- Checked for missing values, incorrect data types, and duplicates.
- These checks are necessary to avoid unexpected results during analysis.

* Step 2: Transform the data
1. Combined two datasets to create one comprehensive dataset.
2. Standardized date formats to ensure consistency.
3. Aggregated duplicate rows (same Id and date) by taking the mean, assuming the difference has meaning.
4. Corrected `TotalDistance` based on `TrackerDistance + LoggedActivitiesDistance`, since original values were inconsistent.
5. Removed the incorrect `TotalDistance` column and kept `CalculatedTotalDistance`.
6. Created a new CSV file from the cleaned dataset for analysis.
7. Checked overall data summary (mean, sum, etc.) to understand the data distribution.
8. Added a 'WeekDay' column extracted from 'ActivityDate' for further analysis.
'''
