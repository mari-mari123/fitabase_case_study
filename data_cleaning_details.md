# Prepare
1. Task
* Download data and store it appropriately.
* Identify how it’s organized.
* Sort and filter the data.
* Determine the credibility of the data.

2. The Place Where The Data Are Stored
* They are stored in local
file path for the data from March 12th to April 11th: Documents/Data Analyst/fitabaseData/mturkfitbit_export_3.12.16-4.11.16
file path for the data from April 12th to May 12th: Documents/Data Analyst/fitabaseData/mturkfitbit_export_4.12.16-5.12.16

3. How The Data Is Organized
* 'dailyActivity_merged.csv' are long format
* Each row has the record of one day's activity divided by Id.

4. Sort And Filter The Data
* Marge two separate file ('Fitabase Data 3.12.16-4.11.16/dailyActivity_merged.csv' and 'Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv')
``` python
import pandas as pd

# data from March to April
df_daily_april = pd.read_csv('data/raw_data/mturkfitbit_export_3.12.16-4.11.16/Fitabase Data 3.12.16-4.11.16/dailyActivity_merged.csv')

# data from April to May
df_daily_may = pd.read_csv('data/raw_data/mturkfitbit_export_4.12.16-5.12.16/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv)

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
1. Task
* Check the data for errors.
* Choose your tools.
* Transform the data so you can work with it effectively.
* Document the cleaning process.

2. Check The Data For Errors.
I have already checked the following during the prepare phase:
* Check for missing values -> None
* Check for date types
* Check for duplicates -> There are duplicates with the same date and same Id, but different values.

3. Choose Your Tools.
I chose Python because:
* It is easier to manipulate data.
* I am not affected by limitations such as data size constraints.

4. Transform The Data So You Can Work With It Effectively.
Documented below.

5. Document The Cleaning Process. (include Transform The Data)
#### Step 1: Check the data for errors
- Checked for missing values, incorrect data types, and duplicates.
- These checks are necessary to avoid unexpected results during analysis.

#### Step 2: Transform the data
1. Combined two datasets to create one comprehensive dataset.
```python
df_combine = pd.concat([df_daily_april, df_daily_may], ignore_index=True)
```

2. Standardized date formats to ensure consistency.
```python
duplicates = df_combine[df_combine.duplicated(subset=['Id', 'ActivityDate'], keep=False)]
```

3. Aggregated duplicate rows (same Id and date) by taking the mean, assuming the difference has meaning.
```python
df_grouped = df_combine.groupby(['Id', 'ActivityDate']).mean().reset_index()
duplicates_grouped = df_grouped[df_grouped.duplicated(subset=['Id', 'ActivityDate'], keep=False)]
```

4. Corrected `TotalDistance` based on `TrackerDistance + LoggedActivitiesDistance`, since original values were inconsistent.
```python
df_grouped['TotalDistance'] = round(df_grouped['TotalDistance'],2)
df_grouped['CalculatedTotalDistance'] = round(df_grouped['TrackerDistance'] + df_grouped['LoggedActivitiesDistance'],2)
not_equal_total_distance = df_grouped[df_grouped['CalculatedTotalDistance'] != df_grouped['TotalDistance']]
df_grouped['TotalDistance'] = df_grouped['CalculatedTotalDistance']
```

5. Removed the incorrect `TotalDistance` column and kept `CalculatedTotalDistance`.
```python
df_grouped_without_TotalDistance = df_grouped[column_without_TotalDistance]
```

6. Created a new CSV file from the cleaned dataset for analysis.
```python
df_grouped_without_TotalDistance.to_csv('data/daily_activity_data.csv', index = False)
df_daily = pd.read_csv('data/daily_activity_data.csv')
```

7. Checked overall data summary (mean, sum, etc.) to understand the data distribution.
```python
print(f"daily_activity_data: {df_daily.Id.nunique()} unique users")
summary = df_daily.describe()
df_by_Id_sum = round(df_daily[column_without_date].groupby('Id').sum(), 2)
df_by_Id_mean = round(df_daily[column_without_date].groupby('Id').mean(), 2)
```
```bash
------------Unique_user-----------
daily_activity_data: 35 unique users
```
```bash
------------Summary-----------
                 Id    TotalSteps  TrackerDistance  LoggedActivitiesDistance  ...  LightlyActiveMinutes  SedentaryMinutes     Calories  CalculatedTotalDistance
count  1.373000e+03   1373.000000      1373.000000               1373.000000  ...           1373.000000       1373.000000  1373.000000              1373.000000
mean   4.782326e+09   7312.367808         5.214483                  0.128591  ...            186.353241        997.386380  2279.630736                 5.343044
std    2.381544e+09   5174.307775         3.949408                  0.695630  ...            112.771702        307.157986   729.943107                 4.097995
min    1.503960e+09      0.000000         0.000000                  0.000000  ...              0.000000          0.000000     0.000000                 0.000000
25%    2.320127e+09   3271.000000         2.230000                  0.000000  ...            114.000000        732.000000  1799.000000                 2.260000
50%    4.445115e+09   7007.000000         4.940000                  0.000000  ...            195.000000       1058.000000  2115.000000                 4.950000
75%    6.962181e+09  10544.000000         7.480000                  0.000000  ...            260.000000       1246.000000  2766.000000                 7.630000
max    8.877689e+09  36019.000000        28.030001                  6.727057  ...            720.000000       1440.000000  4900.000000                28.030000

```
```bash
------------Sum by Id-----------
            TotalSteps  TrackerDistance  LoggedActivitiesDistance  ...  SedentaryMinutes  Calories  CalculatedTotalDistance
Id                                                                 ...
1503960366    590096.0           382.32                      0.00  ...           41300.0   89419.5                   382.32
1624580081    250965.0           168.74                      0.00  ...           62329.0   70620.0                   168.74
1644430081    311237.0           226.35                      0.00  ...           45198.0  113503.0                   226.35
1844505072    120320.5            79.56                      0.00  ...           49065.5   66954.5                    79.55
1927972279     54219.0            37.55                      0.00  ...           51827.5   92824.0                    37.55
```
```bash
------------Mean by Id-----------
            TotalSteps  TrackerDistance  LoggedActivitiesDistance  ...  SedentaryMinutes  Calories  CalculatedTotalDistance
Id                                                                 ...
1503960366    12042.78             7.80                      0.00  ...            842.86   1824.89                     7.80
1624580081     5121.73             3.44                      0.00  ...           1272.02   1441.22                     3.44
1644430081     7780.92             5.66                      0.00  ...           1129.95   2837.58                     5.66
1844505072     2864.77             1.89                      0.00  ...           1168.23   1594.15                     1.89
1927972279     1290.93             0.89                      0.00  ...           1233.99   2210.10                     0.89
```

8. Added a 'WeekDay' column extracted from 'ActivityDate' for further analysis.
```python
df_daily['WeekDay'] = df_daily['ActivityDate'].dt.day_name()
```

6. Summary of Cleaning Process
* Combined and cleaned two datasets.
* Standardized date format for consistency.
* Aggregated duplicate rows.
* Corrected TotalDistance based on logical calculation.
* Created a clean dataset ready for analysis.
* Generated statistical summaries.
* Added 'WeekDay' column for temporal analysis.

7. Conclusion
This process ensures that the dataset is clean, consistent, and ready for reliable analysis. Each step was carefully executed and documented to ensure transparency and reproducibility.
