# Installing and loading common libraries
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Load your CSV files
df_daily = pd.read_csv('daily_activity_data_analyze.csv')

# 1. Aggregate your data so it’s useful and accessible.
# 2. Organize and format your data.
# ----------------------------
## stain the weekday order
week_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
df_daily['WeekDay'] = pd.Categorical(df_daily['WeekDay'], categories=week_order, ordered=True)


## total by weekday
sum_by_weekday = df_daily[['TotalSteps','CalculatedTotalDistance','Calories','WeekDay']].groupby('WeekDay').sum()
sum_by_weekday = sum_by_weekday.rename(columns={'TotalSteps': 'Total Steps', 'CalculatedTotalDistance': 'Total Distance', 'Calories': 'Total Calories'})
# print(sum_by_weekday) # Debugging only

## mean by weekday
mean_by_weekday = df_daily[['TotalSteps','CalculatedTotalDistance','Calories','WeekDay']].groupby('WeekDay').mean()
mean_by_weekday = mean_by_weekday.rename(columns={'TotalSteps': 'Mean Steps', 'CalculatedTotalDistance': 'Mean Distance', 'Calories': 'Mean Calories'})
# print(mean_by_weekday) # Debugging only

# ----------------------------
def classyfy_day(day):
  if day in ['Saturday','Sunday']:
    return 'Weekend'
  else:
    return 'Weekday'

df_daily['Daytype'] = df_daily['WeekDay'].apply(classyfy_day)

## mean by weekday vs weekend
mean_by_daytype = df_daily.groupby(['Daytype'])[['TotalSteps','CalculatedTotalDistance','Calories']].mean()
mean_by_daytype = mean_by_daytype.rename(columns={'CalculatedTotalDistance': 'TotalDistance'})
# print(mean_by_daytype) # Debugging only

## # of rows by daytype
count_by_daytype = df_daily.groupby(['Daytype']).size().reset_index()
count_by_daytype.columns = ['Daytype', 'Number of Date']
# print(count_by_daytype) # Debugging only

# ----------------------------
## add Week column
df_daily['ActivityDate'] = pd.to_datetime(df_daily['ActivityDate'])
df_daily['Week'] = df_daily['ActivityDate'].dt.isocalendar().week
df_daily['Month'] = df_daily['ActivityDate'].dt.month


## total by week, month
sum_by_week = df_daily.groupby('Week')[['TotalSteps','CalculatedTotalDistance','Calories']].sum()
sum_by_week = sum_by_week.rename(columns={'TotalSteps': 'Total Steps', 'CalculatedTotalDistance': 'Total Distance', 'Calories': 'Total Calories'})
# print(sum_by_week) # Debugging only

sum_by_month = df_daily.groupby('Month')[['TotalSteps','CalculatedTotalDistance','Calories']].sum()
sum_by_month = sum_by_month.rename(columns={'TotalSteps': 'Total Steps', 'CalculatedTotalDistance': 'Total Distance', 'Calories': 'Total Calories'})
# print(sum_by_month) # Debugging only

## mean by week, month
mean_by_week = df_daily.groupby('Week')[['TotalSteps','CalculatedTotalDistance','Calories']].mean()
mean_by_week = mean_by_week.rename(columns={'TotalSteps': 'Mean Steps', 'CalculatedTotalDistance': 'Mean Distance', 'Calories': 'Mean Calories'})
# print(mean_by_week) # Debugging only

mean_by_month = df_daily.groupby('Month')[['TotalSteps','CalculatedTotalDistance','Calories']].mean()
mean_by_month = mean_by_month.rename(columns={'TotalSteps': 'Mean Steps', 'CalculatedTotalDistance': 'Mean Distance', 'Calories': 'Mean Calories'})
# print(mean_by_month) # Debugging only

## # of rows by week, month
count_by_week = df_daily.groupby(['Week']).size()
count_by_week.columns = ['Week Number', 'Number of Date in a Week']
count_by_month = df_daily.groupby(['Month']).size()
count_by_month.columns = ['Month', 'Number of Date in a Month']
# print(count_by_week) # Debugging only
# print(count_by_month)

# ----------------------------
# 3. Perform calculations.
## total, mean, max min, rate of activity_day by Id
column_without_date = [
  'TotalSteps', 'TrackerDistance', 'LoggedActivitiesDistance', 'VeryActiveDistance', 'ModeratelyActiveDistance', 'LightActiveDistance', 'SedentaryActiveDistance', 'VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes', 'Calories', 'CalculatedTotalDistance'
  ]
sum_by_id = df_daily.groupby(['Id'])[column_without_date].sum()
mean_by_id = df_daily.groupby(['Id'])[column_without_date].mean()
max_by_id = df_daily.groupby(['Id'])[column_without_date].max()
min_by_id = df_daily.groupby(['Id'])[column_without_date].min()


activdate_by_id = df_daily.groupby(['Id'])[['ActivityDate']].size()
date_start = pd.to_datetime('2016-03-12')
date_end = pd.to_datetime('2016-05-12')
diff_date = (date_end-date_start).days + 1
rate_activdate_by_id = (activdate_by_id / diff_date) * 100

# print(sum_by_id) # Debugging only
# print(mean_by_id)
# print(max_by_id)
# print(min_by_id)
# print(activdate_by_id)
# print(rate_activdate_by_id)

## average of VeryActiveMinutes, FairlyActiveMinutes, LightlyActiveMinutes
variety_of_active = df_daily[['VeryActiveMinutes','FairlyActiveMinutes','LightlyActiveMinutes']].mean()
variety_of_active = variety_of_active.rename(index={'VeryActiveMinutes': 'Average Very Active Minutes', 'FairlyActiveMinutes': 'Average Fairly Active Minutes','LightlyActiveMinutes': 'Average Lightly Active Minutes'})
# print(variety_of_active) # Debugging only

## rate of VeryActiveMinutes, FairlyActiveMinutes, LightlyActiveMinutes, SedentaryMinutes
total_of_VeryActiveMinutes = df_daily['VeryActiveMinutes'].sum()
total_of_FairlyActiveMinutes = df_daily['FairlyActiveMinutes'].sum()
total_of_LightlyActiveMinutes = df_daily['LightlyActiveMinutes'].sum()
total_of_SedentaryMinutes = df_daily['SedentaryMinutes'].sum()
total_activity_min = total_of_VeryActiveMinutes + total_of_FairlyActiveMinutes + total_of_LightlyActiveMinutes + total_of_SedentaryMinutes
rate_very = (total_of_VeryActiveMinutes/total_activity_min)*100
rate_fairly = (total_of_FairlyActiveMinutes/total_activity_min)*100
rate_lightly = (total_of_LightlyActiveMinutes/total_activity_min)*100
rate_sedentary = (total_of_SedentaryMinutes/total_activity_min)*100
total_rate_activity = rate_very + rate_fairly + rate_lightly + rate_sedentary
rate_activity_min = {'Rate': [rate_very, rate_fairly, rate_lightly, rate_sedentary, total_rate_activity]}
df_rate_activity_min= pd.DataFrame(data=rate_activity_min, index=['Very Active','Failrly Activity','Lightly Activity','Sedentary Activity','Total'])
# print(df_rate_activity_min) # Debugging only

## average calories by date
total_calories_by_date = df_daily.groupby('ActivityDate')['Calories'].mean().reset_index()
total_calories_by_date.columns = ['Activity Date', 'Average Calories']
# print(total_calories_by_date) # Debugging only

## rate active date
total_date = ((dt.date(2016,5,12) - dt.date(2016,3,12)).days + 1) * 35 #35 unique users
total_active_date = df_daily['ActivityDate'].count()
rate_active_date = (total_active_date / total_date) * 100
rate_none_active_date = ((total_date-total_active_date)/total_date)*100
data_active_date = {'Rate': [rate_active_date,rate_none_active_date,rate_active_date+rate_none_active_date]}
df_rate_active_date = pd.DataFrame(data=data_active_date, index=['Active Date','Non Active Date','Total'])
# print(df_rate_active_date) # Debugging only

sum_active_min_weekday = df_daily.groupby(['WeekDay'])[['VeryActiveMinutes','FairlyActiveMinutes','LightlyActiveMinutes','SedentaryMinutes']].sum()
# print(sum_active_min_weekday) # Debugging only
mean_active_min_weekday = df_daily.groupby(['WeekDay'])[['VeryActiveMinutes','FairlyActiveMinutes','LightlyActiveMinutes','SedentaryMinutes']].mean()
# print(mean_active_min_weekday) # Debugging only
sum_active_min_month = df_daily.groupby(['Month'])[['VeryActiveMinutes','FairlyActiveMinutes','LightlyActiveMinutes','SedentaryMinutes']].sum()
# print(sum_active_min_month) # Debugging only
mean_active_min_month = df_daily.groupby(['Month'])[['VeryActiveMinutes','FairlyActiveMinutes','LightlyActiveMinutes','SedentaryMinutes']].mean()
# print(mean_active_min_month) # Debugging only

# 4. Identify trends and relationships.
## 1. correlation
correlation = df_daily[['TotalSteps','VeryActiveDistance','VeryActiveMinutes', 'Calories', 'CalculatedTotalDistance']].corr()
# print(correlation) # Debugging only

correlation_avtivity = df_daily[['TrackerDistance', 'VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes']].corr()
# print(correlation_avtivity) # Debugging only

correlation_activity_weekday = df_daily.groupby(['WeekDay'])[['TotalSteps','VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes']].corr()
# print(correlation_activity_weekday) # Debugging only

correlation_activity_month = df_daily.groupby(['Month'])[['TotalSteps','VeryActiveMinutes', 'FairlyActiveMinutes', 'LightlyActiveMinutes', 'SedentaryMinutes']].corr()
# print(correlation_activity_month) # Debugging only

## 2. comparison among users
user_median_steps = df_daily['TotalSteps'].median()

'''
median of TotalStep => 7007.000000 from Process phase
my assumption:
up to 7007 => active user
less than 7007 => non active user
'''
active_users = mean_by_id[mean_by_id['TotalSteps'] >= 7007]
non_active_users = mean_by_id[mean_by_id['TotalSteps'] < 7007]

active_users_summary = active_users.describe()
non_active_users_summary = non_active_users.describe()

# print(active_users_summary) # Debugging only
# print(non_active_users_summary)


## 3. visuallization of trend
### basic settings
plt.figure(figsize=(5,5))

# ## Weekday
# ##needed data to make chaets

weekday_sum_steps = [_ for _ in sum_by_weekday['Total Steps']]
weekday_sum_calories = [_ for _ in sum_by_weekday['Total Calories']]

weekday_average_steps = [round(_) for _ in mean_by_weekday['Mean Steps']]
weekday_average_calories = [_ for _ in mean_by_weekday['Mean Calories']]

## Total Steps

def millions(x, pos):
    return f'{x * 1e-6:.1f}M'
sum_bar_steps = plt.bar(week_order, weekday_sum_steps)
labels = [f"{v / 1_000_000:.2f}M" for v in weekday_sum_steps]
plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))
plt.bar_label(sum_bar_steps, labels=labels, padding=6)
plt.gca().set_ylim(1_200_000, 1750000)
plt.title('Total Steps by Weekday', size=15)
plt.xlabel('Weekday', size=15)
plt.ylabel('Total Steps (Million)', size=15)
plt.xticks(rotation=60)
plt.tight_layout()
plt.savefig("total_steps_by_weekday.png", dpi=300)
plt.show()

mean_step_bar = plt.bar(week_order, weekday_average_steps)
plt.bar_label(mean_step_bar, padding=6)
plt.gca().set_ylim(6500,8000)
plt.title('Average Steps by Weekday', size=15)
plt.xlabel('Weekday', size=15)
plt.ylabel('Average Steps', size=15)
plt.xticks(rotation=60)
plt.ticklabel_format(style='plain',axis='y')
plt.savefig("average_steps_by_weekday.png", dpi=300)
plt.show()

## Calories
sum_bar_calories = plt.bar(week_order, weekday_sum_calories)
plt.bar_label(sum_bar_calories, padding=6)
plt.gca().set_ylim(400000,500000)
plt.title('Total Consuming Calories by Weekday', size=15)
plt.xlabel('Weekday', size=15)
plt.ylabel('Total Calories', size=15)
plt.xticks(rotation=60)
plt.ticklabel_format(style='plain',axis='y')
plt.savefig("total_consuming_calories_by_weekday.png", dpi=300)
plt.show()


mean_calory_bar = plt.bar(week_order, weekday_average_calories)
plt.bar_label(mean_calory_bar, padding=6)
plt.gca().set_ylim(2000,2500)
plt.title('Average Consuming Calories by Weekday', size=15)
plt.xlabel('Weekday', size=15)
plt.ylabel('Average Calories', size=15)
plt.xticks(rotation=60)
plt.ticklabel_format(style='plain',axis='y')
plt.savefig("average_consuming_calories_by_weekday.png", dpi=300)
plt.show()


## Daytype
##needed data to make chaets (Since the number of weekdays in the dataset is clearly higher, I excluded total values and focused on averages for a fair comparison.)
daytype_mean_steps = [_ for _ in mean_by_daytype['TotalSteps']]
daytype_mean_calirues = [_ for _ in mean_by_daytype['Calories']]
day_type = ['Weekday','Weekend']

dtype_bar_steps = plt.bar(day_type, daytype_mean_steps)
plt.bar_label(dtype_bar_steps, padding=6)
plt.gca().set_ylim(6000,8000)
plt.title('Average Steps by Daytype', size=15)
plt.xlabel('Daytype',size=15)
plt.ylabel('Average Steps', size=15)
plt.savefig("average_steps_by_daytype.png", dpi=300)
plt.show()

dtype_bar_calories = plt.bar(day_type, daytype_mean_calirues)
plt.bar_label(dtype_bar_calories, padding=6)
plt.gca().set_ylim(2000,2400)
plt.title('Average Calories by Daytype', size=15)
plt.xlabel('Daytype',size=15)
plt.ylabel('Average Consuming Calories', size=15)
plt.savefig("average_calories_by_daytype.png", dpi=300)
plt.show()

## Month
##needed data to make chaets(Since the number of weekdays in the dataset is clearly higher, I excluded total values and focused on averages for a fair comparison.)
month_mean_steps = [_ for _ in mean_by_month['Mean Steps']]
month_mean_calories = [_ for _ in mean_by_month['Mean Calories']]
month = ['March','April','May']

m_bar_steps = plt.bar(month, month_mean_steps)
plt.bar_label(m_bar_steps, padding=6)
plt.gca().set_ylim(4000,8000)
plt.title('Average Steps by Month', size=15)
plt.xlabel('Month',size=15)
plt.ylabel('Average Consuming Calories', size=15)
plt.savefig("average_steps_by_month.png", dpi=300)
plt.show()

m_bar_calories = plt.bar(month, month_mean_calories)
plt.bar_label(m_bar_calories, padding=6)
plt.gca().set_ylim(2000,2400)
plt.title('Average Calories by Month', size=15)
plt.xlabel('Month',size=15)
plt.ylabel('Average Consuming Calories', size=15)
plt.savefig("average_calories_by_month.png", dpi=300)
plt.show()


## Comparison between Active and Non-active users!
## needed data to make charts
active_user_min = [x for x in active_users['VeryActiveMinutes']]
active_user_steps = [x for x in active_users['TotalSteps']]
active_user_calories = [x for x in active_users['Calories']]
non_active_user_min = [x for x in non_active_users['VeryActiveMinutes']]
non_active_user_steps = [x for x in non_active_users['TotalSteps']]
non_active_user_calories = [x for x in non_active_users['Calories']]

user_calories_median = df_daily['Calories'].median()
user_calories_mean = df_daily['Calories'].mean()


### Distribution of Total Steps
plt.hist(active_user_steps, color='red', label='active user')
plt.hist(non_active_user_steps, color='blue', label='non-active user', histtype='step')
plt.title('Distribution of Total Steps', size=15)
plt.xlabel('Total Steps', size=15)
plt.ylabel('# of Users', size=15)
plt.axvline(user_median_steps, color='green', linestyle='--', linewidth=2, label=f'Median Steps: {int(user_median_steps)}') #to show median steps
plt.legend()
plt.xticks(rotation=60)
plt.savefig("distribution_of_total_steps.png", dpi=300)
plt.show()

### Distribution of Calories
plt.hist(active_user_calories, color='red', label='active user')
plt.hist(non_active_user_calories, color='blue', label='non-active user', histtype='step')
plt.title('Distribution of Calories', size=15)
plt.xlabel('Calories', size=15)
plt.ylabel('# of Users', size=15)
plt.axvline(user_calories_median, color='green', linestyle='--', linewidth=2, label=f'Median Calories: {int(user_calories_median)}') #to show median
plt.axvline(user_calories_mean, color='pink', linestyle='--', linewidth=2, label=f'Mean Calories: {int(user_calories_mean)}') #to show mean
plt.legend()
plt.savefig("distribution_of_calories.png", dpi=300)
plt.show()

## Comparison of VeryActiveMinutes

#### total steps and very active minutes
plt.scatter( x = active_user_steps, y = active_user_min, color = 'red', label = 'active user')
plt.scatter( x = non_active_user_steps, y = non_active_user_min, color = 'blue', label = 'non-active user')
plt.title('Active Users VS Non-active Users', size=15)
plt.xlabel('Total Steps', size=15)
plt.ylabel('Very Active Minutes', size=15)
plt.legend()
plt.savefig("active_users_vs_non-active_users_total_steps.png", dpi=300)
plt.show()

#### calories and vary active minutes
plt.scatter( x = active_user_calories, y = active_user_min, color = 'red', label = 'active user')
plt.scatter( x = non_active_user_calories, y = non_active_user_min, color = 'blue', label = 'non-active user')
plt.title('Active Users VS Non-active Users', size=15)
plt.xlabel('Calories', size=15)
plt.ylabel('Very Active Minutes', size=15)
plt.legend()
plt.savefig("active_users_vs_non-active_users_calories.png", dpi=300)
plt.show()


## 4. summarize overall
'''
correlation result!

                        TotalSteps  VeryActiveDistance  VeryActiveMinutes  Calories  CalculatedTotalDistance
TotalSteps                 1.000000            0.736618           0.675301  0.580400                 0.975968
VeryActiveDistance         0.736618            1.000000           0.833642  0.475322                 0.787515
VeryActiveMinutes          0.675301            0.833642           1.000000  0.590171                 0.700374
Calories                   0.580400            0.475322           0.590171  1.000000                 0.637010
CalculatedTotalDistance    0.975968            0.787515           0.700374  0.637010                 1.000000

                      TrackerDistance  VeryActiveMinutes  FairlyActiveMinutes  LightlyActiveMinutes  SedentaryMinutes
TrackerDistance              1.000000           0.688525             0.339173              0.541313         -0.312943
VeryActiveMinutes            0.688525           1.000000             0.233631              0.099376         -0.182369
FairlyActiveMinutes          0.339173           0.233631             1.000000              0.114613         -0.197647
LightlyActiveMinutes         0.541313           0.099376             0.114613              1.000000         -0.469737
SedentaryMinutes            -0.312943          -0.182369            -0.197647             -0.469737          1.000000
'''

'''
By weekday, days except for Sunday are same trends regarding to total steps. However, the level of consuming calories are almost similar, so it indicates that users are doing additional activiy, not walking.
By weektype, weekday is more active than weekend only respect to total steps because Sunday is the lowest steps, while their consumig calories are almost same because users consume it even more not by walking.
By month, March have a different trend with April and May regarding total steps, while the trending on calories are almost same, so it implys that users did additional activity on March.
We also compared between active and non-active users. Obviously, active users walk more steps than non-active users, but the distribution of consuming calories depends on the users. Of course, non-active users tend to be left side of the graph, and active ones tend to be right of one, but some non-active users consume calories more than the mean and median of it. About the relationship between total steps and very active miniutes, non-active users share almost same trends looking like positive correlation. On the other hand, that of active users are more variable. Overall, the correlation between total steps and very active miniutes are positive correlation, so it indicates users are using this device for recording walking steps.
'''
