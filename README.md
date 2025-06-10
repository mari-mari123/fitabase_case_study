# Bellabeat Case Study
![pexels-daniel-reche-718241-3601094](https://github.com/user-attachments/assets/6355cbf3-002c-4509-b669-03dcff715784)
Photo by [Daniel Reche](https://www.pexels.com/photo/person-jogging-3601094/)

## Introduction
###  Analysis overview
We used the Fitabase dataset, which contains smart device usage data, to uncover insights that could inform Bellabeat’s marketing strategy.
###  Project information
Bellabeat’s Chief Creative Officer, Urška Sršen, requested the marketing analytics team to analyze how consumers use smart devices (excluding Bellabeat products) and to provide actionable insights for improving Bellabeat’s marketing approach.
###  About the company
Bellabeat is a high-tech company that creates health-focused smart products for women. Although currently a small player, the company has significant potential to grow in the competitive smart device market.

## Ask
### 1. Task
- [x] Identify the business task
- [x] Consider key stakeholders

### 2. Business Tasks
Our task is to identify usage trends of non-Bellabeat smart devices and understand how consumers engage with them. Based on these insights, we aim to recommend strategies to enhance Bellabeat's marketing.

### 3. Key Stakeholders

* Urška Sršen: Bellabeat’s co founder and Chief Creative Officer
* Sando Mur: Mathematician and Bellabeat cofounder; key member of the Bellabeat executive team
* Bellabeat marketing analytics team: A team of data analysts responsible for collecting, analyzing, and reporting data that helps guide Bellabeat’s marketing strategy.

### 4. Business Questions
* What are users’ activity patterns over time?
* How do activity levels relate to calorie consumption?
* Are there differences between active and non-active users?

## Prepare
* Combined two monthly datasets and removed duplicates by taking daily means for each user.
* Checked for missing values (none found) and ensured data types were consistent.
* Performed range checks (e.g., negative values, outliers).
* Verified logical consistency (e.g., TotalDistance ≈ Tracker + LoggedActivities).
* Final cleaned dataset: daily_activity_data.csv (1372 records, 35 users, March–May 2016)

📝 See full cleaning process in [data_cleaning_details.md](https://github.com/mari-mari123/fitabase_case_study/blob/develop/data_cleaning_details.md)

🧑‍💻 See full code in [prepare.py](https://github.com/mari-mari123/fitabase_case_study/blob/develop/scripts/prepare.py)

* envirenment
  * Device: Apple M1
  * OS: macOS 15.0
  * Python: 3.13.2
  * pip: 25.0

## Process
* Cleaned data using Python (pandas).
* Created new columns such as WeekDay, Month, and CalculatedTotalDistance.
* Removed extreme outliers (e.g., over 100,000 steps/day).
* Standardized fields and exported final version for analysis.

📝 See full cleaning process in [data_cleaning_details.md](https://github.com/mari-mari123/fitabase_case_study/blob/develop/data_cleaning_details.md)

🧑‍💻 See full code in [process.py](https://github.com/mari-mari123/fitabase_case_study/blob/develop/scripts/process.py)

## Analyze
📝 See full results step by step in [analyze.ipynb](https://github.com/mari-mari123/fitabase_case_study/blob/develop/notebooks/analyze.ipynb)

🧑‍💻 See full code in [analyze.py](https://github.com/mari-mari123/fitabase_case_study/blob/develop/scripts/analyze.py)

📈 See all charts in [images](https://github.com/mari-mari123/fitabase_case_study/tree/develop/images)

### 1. Key tasks
- [x] Aggregate your data so it’s useful and accessible.
- [x] Organize and format your data.
- [x] Perform calculations.
- [x] Identify trends and relationships.

### 2. Results
#### Analysis By Weekday
* Sunday has the lowest total steps (approx. 1.28 million), while Saturday has the highest (approx. 1.54 million).
* From Monday to Friday, steps are stable (avg. ~1.4 million).
* However, calories burned on Sunday remain high (~430,000), suggesting other forms of physical activity.
* Sunday also shows the highest sedentary time and lowest very active minutes.

#### Analysis By Weektype
* Users walk more on weekdays than on weekends.
* This difference is mainly due to Sunday, which significantly lowers the weekend average step count.
* Average calories burned are nearly the same:
  * Weekdays: ~2280 kcal
  * Weekends: ~2277 kcal
* Despite fewer steps on weekends, calorie burn remains stable.
* This indicates users may engage in alternative physical activities or burn calories through their basal metabolic rate.

#### Monthly Trends
* March has the lowest average steps (~5,000), while April and May average over 7,000 steps—a difference of about 2,000 steps.
* Despite lower activity in March, average calorie burn remains stable at around 2,200 across all three months.
* In March, users were more sedentary (average of 1,162 minutes) and spent less time being very active (7 minutes), compared to ~900 sedentary minutes and ~20 very active minutes in April and May.
* This suggests users maintained similar calorie expenditure in March through other forms of activity or metabolic differences.

#### Active VS Non-active Users

* Users were classified as active if their average steps ≥ 7007, and non-active if below.
* Active users had greater variation in steps (some > 14,000 steps/day), while non-active users had more evenly distributed and lower step counts.
* Calorie consumption distributions did not differ significantly between the groups:
  * Some non-active users burned more calories than the overall average.
  * Some active users burned fewer calories than expected.
* This suggests that calorie burn depends not just on steps, but also on individual traits (e.g., weight, muscle mass, metabolism, exercise type).
* Regarding steps vs very active minutes:
  * Non-active users show a clear positive correlation.
  * Active users show more variability.
  * Overall correlation ≈ 0.7, indicating a moderately strong relationship between steps and very active minutes.
* This implies users mainly use the device to track walking, but walking is not the only source of calorie expenditure.

#### Additional Notes
* **Activity Type by Weekday and Month**:
Sunday and March show higher sedentary times and fewer very active minutes, indicating less intense activity.

* **Rate of Active Dates**:
The active date rate is about 63%, meaning users did not record activity every day, which should be considered in analysis.

#### Conclusion
* Weekday step trends are consistent, except for Sunday, which shows the lowest.
* Calorie consumption remains stable across weekdays, suggesting other activities contribute to calorie burn.
* Weekends have lower step counts (mainly due to Sunday), but calories burned remain similar to weekdays.
* In March, users took fewer steps but still burned similar calories—implying alternative activities or individual differences.
* Active user walk more, but calorie consumption doesn't directly match activity levels.
* Some non-active users burn more calories than active ones.
* There’s a positive correlation (≈0.7) between steps and very active minutes, especially among non-active users.
* The device is primarily used to track walking, but other factors influence calorie burn.

## Share
### 1. Key tasks
- [x] Determine the best way to share your findings.
- [x] Create effective data visualizations.
- [x] Present your findings.
- [x] Ensure your work is accessible.

### 2. Deliverable
[Presentation](https://github.com/mari-mari123/fitabase_case_study/blob/develop/Presentation.pdf)

## Act
### 1. Key tasks
- [x] Create your portfolio.
- [x] Add your case study.
- [x] Practice presenting your case study to a friend or family member.

### 2. Deliverable
[GitHub Repository](https://github.com/mari-mari123/fitabase_case_study)

## Data Source

This project uses the **FitBit Fitness Tracker Data** made available by [Arash Nik](https://www.kaggle.com/datasets/arashnic/fitbit) on Kaggle.
* Dataset title: *FitBit Fitness Tracker Data*
* Released: 2016
* License: [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)
