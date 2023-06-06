import csv
import statistics
from scipy import stats
import numpy as np
from scipy.stats import chi2_contingency

# Open the CSV file for reading
with open('data_bachelor.csv', 'r', newline='') as file:
    reader = csv.reader(file, delimiter=';')
    # Skip the header row
    next(reader)
    # Create a list of the remaining rows
    rows = [row for row in reader]

    # Converting col0, col5-col8, col11-14 and col17-22 into a list of ints
    for j in list(range(0,1)) + list(range(5,9)) + list(range(11,15)) + list(range(17,23)):
        for i in range(len(rows)):
            if rows[i][j] == "": # if there is no motive/consequence
                rows[i][j] = []
            elif rows[i][j][-1] == ",": # if it ends with "," (excel writes 5,10 as 5,1 so was needed)
                rows[i][j] = rows[i][j][:-1]
                column_str = rows[i][j]
                column_list = column_str.split(",")
                column_int_list = list(map(int, column_list))
                rows[i][j] = column_int_list
            else: # makes it to a list and converts every element to int
                column_str = rows[i][j]
                column_list = column_str.split(",")
                column_int_list = list(map(int, column_list))
                rows[i][j] = column_int_list
print("-----------------------------------------------------------")

#DEL 1: WHAT IS OUR MOTIVE? ##################################################################################
# Number of apps with hedonic motive
num_hedonic_motive = 0
for i in range(len(rows)):
    for j in [5, 11, 17]:
        if (any(x in [2,3,4,5,6] for x in rows[i][j])):
            num_hedonic_motive +=1
print("Number of apps with hedonic motives:", num_hedonic_motive)

# Number of apps with eudaimonic motive
num_hedonic_motive = 0
for i in range(len(rows)):
    for j in [5, 11, 17]:
        if (any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][j])):
            num_hedonic_motive +=1
print("Number of apps with eudaimonic motives:", num_hedonic_motive)

# Distribution between all hedonic answers
motives = {
    2: "relax",
    3: "enjoyment",
    4: "taking it easy",
    5: "pleasure",
    6: "fun",
    7: "doing what you believe in",
    8: "pursuing excellence",
    9: "use best in yourself",
    10: "developing a skill",
    11: "productivity",
    12: "work" }

counts = {}
for i in range(len(rows)):
    for x in rows[i][5]:
        if x in range(2, 13):
            if x not in counts:
                counts[x] = 0
            counts[x] += 1

for i in range(2, 13):
    print("Number of apps for", motives[i], ":", counts.get(i, 0))

# How many obtaining at least their goal motives for top 1 app
count = 0
for i in range(len(rows)):
    if all(elem in str(rows[i][6]) for elem in str(rows[i][5])) and (len(rows[i][5]) != 0) and (len(rows[i][6]) != 0):
        count += 1
print("Persons obtaining their motives and also more for top 1:", count)

# How many obtaining at least their goal motives for top 2 app
count = 0
for i in range(len(rows)):
    if all(elem in str(rows[i][12]) for elem in str(rows[i][11])) and (len(rows[i][11]) != 0) and (len(rows[i][12]) != 0):
        count += 1
print("Persons obtaining their motives and also more for top 2:", count)

# How many obtaining at least their goal motives for top 1 app hed
count = 0
for i in range(len(rows)):
    if all(elem in str(rows[i][18]) for elem in str(rows[i][17])) and (len(rows[i][5]) != 0) and (len(rows[i][6]) != 0) and any(x in [2, 3, 4, 5, 6] for x in rows[i][17]):
        count += 1
print("Persons obtaining their motives and also more, top1,hed:", count)

# How many obtaining at least their goal motives for top 3 app eud
count = 0
for i in range(len(rows)):
    if all(elem in str(rows[i][18]) for elem in str(rows[i][17])) and (len(rows[i][17]) != 0) and (len(rows[i][18]) != 0) and (any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][17])):
        count += 1
print("Persons obtaining their motives and also more, top3, eud:", count)

# How many obtaining at least their goal motives for top 1 app and having eudaimonic motives
count = 0
for i in range(len(rows)):
    if all(elem in str(rows[i][6]) for elem in str(rows[i][5])) and (len(rows[i][5]) != 0) and (len(rows[i][6]) != 0) and (any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][5])):
        count += 1
print("Persons obtaining their motives and also more, top1, eud:", count)

# How many obtaining at least their goal motives for top 2 app and having eudaimonic motives
count = 0
for i in range(len(rows)):
    if all(elem in str(rows[i][12]) for elem in str(rows[i][11])) and (len(rows[i][12]) != 0) and (len(rows[i][11]) != 0) and (any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][11])):
        count += 1
print("Persons obtaining their motives and also more, top2, eud:", count)
print("-----------------------------------------------------------")

#DEL 2: SAMMENHÆNG MELLEM MOTIV OG VELVÆRE? ##################################################################################
# Check how many has a hedonic motive on top 1 app
num_hedonic_motive = 0
for i in range(len(rows)):
    if any(x in [2, 3, 4, 5, 6] for x in rows[i][5]):
        num_hedonic_motive +=1
print("People with hedonic motives for top 1 app:", num_hedonic_motive)

# Check how many has a eudaimonic motive for their top 1 app (i take work as a part of eudaimonia)
num_eudaimonic_motive = 0
for i in range(len(rows)):
    if any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][5]):
        num_eudaimonic_motive +=1
print("People with eudaimonic motives for top 1 app:", num_eudaimonic_motive)

# Check how many having hedonic motives and have problems for top 1 app
count=0
for i in range(len(rows)):
    if any(x in [2, 3, 4, 5, 6] for x in rows[i][5]) and any(x in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11] for x in rows[i][7]):
        count+=1
print("Having hedonic motive and consequences for top 1 app:", count)

# Check how many having eudaimonic motives and have problems for top 1 app
count=0
for i in range(len(rows)):
    if any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][5]) and any(x in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11] for x in rows[i][7]):
        count+=1
print("Having eudaimonic motive and consequences for top 1 app:", count)

# chi-i-anden test of motive and negative consequences:
# krydstabel med observerede værdier
observed = [[59, 72-59], [24, 31-24]]
chi2, p_value, _, _ = chi2_contingency(observed)
print("Chi-i-anden værdi:", chi2)
print("P-værdi:", p_value)

#psysical problems: 2,3,4,5
#mental problems: 6,7,8
#not classified: 9,10,11

# Check how many having hedonic motives and have physical problems for top 1 app
count=0
for i in range(len(rows)):
    if any(x in [2, 3, 4, 5, 6] for x in rows[i][5]) and any(x in [2, 3, 4, 5] for x in rows[i][7]):
        count+=1
print("Having hedonic motive and physical consequences for top 1 app:", count)
# Check how many having hedonic motives and have physical problems for top 2 app
count=0
for i in range(len(rows)):
    if any(x in [2, 3, 4, 5, 6] for x in rows[i][11]) and any(x in [2, 3, 4, 5] for x in rows[i][13]):
        count+=1
#print("Having hedonic motive and physical consequences for top 2 app:", count)
# Check how many having hedonic motives and have physical problems for top 3 app
count=0
for i in range(len(rows)):
    if any(x in [2, 3, 4, 5, 6] for x in rows[i][17]) and any(x in [2, 3, 4, 5] for x in rows[i][19]):
        count+=1
#print("Having hedonic motive and physical consequences for top 3 app:", count)

# Check how many having hedonic motives and have mental problems for top 1 app
count=0
for i in range(len(rows)):
    if any(x in [2, 3, 4, 5, 6] for x in rows[i][5]) and any(x in [6, 7, 8] for x in rows[i][7]):
        count+=1
print("Having hedonic motive and mental consequences for top 1 app:", count)

# Check how many having eudaimonic motives and have physical problems for top 1 app
count=0
for i in range(len(rows)):
    if any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][5]) and any(x in [2, 3, 4, 5] for x in rows[i][7]):
        count+=1
print("Having eudaimonic motive and physical consequences for top 1 app:", count)

# Check how many having eudaimonic motives and have mental problems
count=0
for i in range(len(rows)):
    if any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][5]) and any(x in [6, 7, 8] for x in rows[i][7]):
        count+=1
print("Having eudaimonic motive and mental consequences:", count)

# chi-i-anden test af motiv og fysiske konsekvenser:
# krydstabel med observerede værdier
observed = [[35, 72-35], [16, 31-16]]
chi2, p_value, _, _ = chi2_contingency(observed)
print("Chi-i-anden værdi:", chi2)
print("P-værdi:", p_value)

# chi-i-anden test af motiv og psykiske konsekvenser:
# krydstabel med observerede værdier
observed = [[16, 72-16], [8, 31-8]]
chi2, p_value, _, _ = chi2_contingency(observed)
print("Chi-i-anden værdi:", chi2)
print("P-værdi:", p_value)

# Check how much time people with hedonic motives spend on apps
times = []
for i in range(len(rows)):
    if any(x in [2, 3, 4, 5, 6] for x in rows[i][5]):
    # computing the time
        if rows[i][4] != "":
            times.append(rows[i][4])
total_hours, total_minutes = 0, 0
for t in times:
    hours, minutes = map(int, t.split('.'))
    total_hours += hours
    total_minutes += minutes
# calculate the total time in minutes
total_minutes += total_hours * 60
# calculate the average time in minutes
average_time = total_minutes / len(times)
# convert average time to hours and minutes
avg_hours = int(average_time // 60)
avg_minutes = int(average_time % 60)
# format the average time as hh:mm
avg_time_str = f"{avg_hours:02d}:{avg_minutes:02d}"
print("Time used on average on apps with hedonic motives:", avg_time_str)

# Check how much time people spend on apps with eudaimonic motives 
times = []
for i in range(len(rows)):
    if any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][5]):
        if rows[i][4] != "":
            times.append(rows[i][4])
total_hours, total_minutes = 0, 0
for t in times:
    hours, minutes = map(int, t.split('.'))
    total_hours += hours
    total_minutes += minutes
total_minutes += total_hours * 60
average_time = total_minutes / len(times)
avg_hours = int(average_time // 60)
avg_minutes = int(average_time % 60)
avg_time_str = f"{avg_hours:02d}:{avg_minutes:02d}"
print("Time used on average on apps with eudaimonic motives:", avg_time_str)
print("-----------------------------------------------------------")

#DEL 3: SAMMENHÆNG MELLEM MOTIV OG TILFREDSHED? ##################################################################################
# What is the avg. satisfaction grade given by hedonic users:
satisfactions_hed = []
for i in range(len(rows)):
    if any(x in [2, 3, 4, 5, 6] for x in rows[i][5]):
        satisfactions_hed.append(rows[i][8])
    if any(x in [2, 3, 4, 5, 6] for x in rows[i][11]):
        satisfactions_hed.append(rows[i][14])
    if any(x in [2, 3, 4, 5, 6] for x in rows[i][17]):
        satisfactions_hed.append(rows[i][20])
# flatten the list
lst = [i[0] for i in satisfactions_hed]
# calculate the average
average = statistics.mean(lst)
print("Avg. satisfaction amoung hedonic users:", average)
# std for hedonic
std = statistics.stdev([val for sublist in satisfactions_hed for val in sublist])
print("Std for hedonic:", std)

# What is the avg. satisfaction grade given by eudaimonic users
satisfactions_eud = [rows[i][j+3] for i in range(len(rows)) for j in [5, 11, 17] if any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][j])]
lst = [i[0] for i in satisfactions_eud]
average = statistics.mean(lst)
print("Avg. satisfaction amoung eudaimonic users:", average)
std = statistics.stdev([val for sublist in satisfactions_eud for val in sublist])
print("Std for eudaimonic", std)

#t-test
t_statistic, p_value = stats.ttest_ind(satisfactions_hed, satisfactions_eud)
print('t-statistic:', t_statistic)
print('p-value:', p_value)

# What apps are reported from eudaimonis users
eud_apps = []
for i in range(len(rows)):
    if any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][5]):
        eud_apps.append(rows[i][3])
    if any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][11]):
        eud_apps.append(rows[i][9])
    if any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][17]):
        eud_apps.append(rows[i][15])
print("Apps reported by eudaimonic users:", eud_apps)
print("-----------------------------------------------------------")

#DEL 4: TILFREDSHED MED MOBILEN GENERELT ##################################################################################
# How satisfies are we with out phones in generel
satisfactions_genereal = []
for i in range(len(rows)):
    satisfactions_genereal.append(rows[i][21])
satisfactions_lst = [i[0] for i in satisfactions_genereal if i]
average = statistics.mean(satisfactions_lst)
print("Average satisfaction in genereal:", average)

# How much do we regret the use on the scale
regrets = []
for i in range(len(rows)):
    regrets.append(rows[i][22])
regrets_lst = [i[0] for i in regrets if i]
average = statistics.mean(regrets_lst)
print("Average regret:", average)

# How much to people with hedonic motives regret
regrets_hed = []
for i in range(len(rows)):
    if any(x in [2, 3, 4, 5, 6] for x in rows[i][5]) or any(x in [2, 3, 4, 5, 6] for x in rows[i][11]) or any(x in [2, 3, 4, 5, 6] for x in rows[i][17]):
        regrets_hed.append(rows[i][22])
lst = [i[0] for i in regrets_hed if i]
average = statistics.mean(lst)
print("Average regret amoung hedonic users:", average)
std = statistics.stdev([val for sublist in regrets_hed for val in sublist])
print("Std for hedonic:", std)

# How much to people with eudaimonic motives regret
regrets_eud = []
for i in range(len(rows)):
    if any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][5]) or any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][11]) or any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][17]):
        regrets_eud.append(rows[i][22])
lst = [i[0] for i in regrets_eud if i]
average = statistics.mean(lst)
print("Average regret amoung eudaimonic users:", average)
std = statistics.stdev([val for sublist in regrets_eud for val in sublist])
print("Std for eudaimonic:", std)

#t-test
t_statistic, p_value = stats.ttest_ind(regrets_hed, regrets_eud)
print('t-statistic:', t_statistic)
print('p-value:', p_value)

#correlation between satisfaction and regret
correlation = np.corrcoef(satisfactions_lst, regrets_lst)
print("Correlation matrix:", correlation)

# choosing all satisfies and check how much avg. regret
reg_lst1 = []
# converting the satisfations to an int list
sat_lst = [] #
for i in range(len(rows)):
    sat_lst.append(rows[i][21])
reg_lst_satisfied = [i[0] for i in sat_lst if i]
for i in range(len(reg_lst_satisfied )):
    if reg_lst_satisfied[i] > 4:
        reg_lst1.append(rows[i][22])
lst2 = [i[0] for i in reg_lst1 if i]
average2 = statistics.mean(lst2)
print("Average regret amoung satisfied users:", average2)

# Why are the unsatisfied users not satisfied - not obtaining their motives?
sat_lst = []
for i in range(len(rows)):
    sat_lst.append(rows[i][21])
sat_lst = [i[0] for i in sat_lst if i]
# getting the ids on the unsatisfied users
not_sat_id = []
for i in range(len(sat_lst)):
    if sat_lst[i] < 4:
        not_sat_id.append(rows[i][0])
not_sat_id = [i[0] for i in not_sat_id if i]
print("Number of people unsatisfied:", len(not_sat_id))
# counting the unsatisfied and obtaining their motives
count = 0
for i in range(len(not_sat_id)):
    if all(elem in str(rows[not_sat_id[i]-1][6]) for elem in str(rows[not_sat_id[i]-1][5])) and all(elem in str(rows[not_sat_id[i]-1][12]) for elem in str(rows[not_sat_id[i]-1][11])) and all(elem in str(rows[not_sat_id[i]-1][18]) for elem in str(rows[not_sat_id[i]-1][17])):
        count += 1
print("Number of people unsatisfied and not obtaining their motives:", len(not_sat_id)-count)

# Why are the unsatisfied users not satisfied - having many consequences?
count = 0
for i in range(len(not_sat_id)):
    if any(x in [2, 3, 4, 5, 6, 7, 8, 10, 11] for x in rows[not_sat_id[i]-1][7]) or any(x in [2, 3, 4, 5, 6, 7, 8, 10, 11] for x in rows[not_sat_id[i]-1][13]) or any(x in [2, 3, 4, 5, 6, 7, 8, 10, 11] for x in rows[not_sat_id[i]-1][19]):
        count += 1
print("Number of people unsatisfied and having consequences:", count)

# What apps are reported from satisfies users
satisfied_apps = []
for row in rows:
    app_indices = [8, 14, 20]  # Indices of columns with consequences
    app_names = [3, 9, 15]     # Indices of columns with app names
    for i in range(len(app_indices)):
        if any(x in [5, 6, 7] for x in row[app_indices[i]]):
            satisfied_apps.append(row[app_names[i]])
print("Apps reported with satisfaction:", satisfied_apps)

print("-----EXTRA------------------------------------------------------")
#EXTRA ##################################################################################
#compare to the satisfied users - how many satisfied and having consequences
sat_id = []
for i in range(len(sat_lst)):
    if sat_lst[i] >= 4:
        sat_id.append(rows[i][0])
sat_id = [i[0] for i in sat_id if i]
print("Number of people satisfied:", len(sat_id))
count = 0
for i in range(len(sat_id)):
    if any(x in [2, 3, 4, 5, 6, 7, 8, 10, 11] for x in rows[sat_id[i]-1][7]) or any(x in [2, 3, 4, 5, 6, 7, 8, 10, 11] for x in rows[sat_id[i]-1][13]) or any(x in [2, 3, 4, 5, 6, 7, 8, 10, 11] for x in rows[sat_id[i]-1][19]):
        count += 1
print("Number of people satisfied and having consequences:", count)

# Check how many has a hedonic motive over all apps
num_hedonic_motive = 0
for i in range(len(rows)):
    if any(x in [2, 3, 4, 5, 6] for x in rows[i][5]) or any(x in [2, 3, 4, 5, 6] for x in rows[i][11]) or any(x in [2, 3, 4, 5, 6] for x in rows[i][17]) :
        #print(rows[i][0])
        num_hedonic_motive +=1
#print("People with hedonic motives:", num_hedonic_motive)

# Check how many has a eudaimonic motive over all apps (i take work as a part of eudaimonia)
num_eudaimonic_motive = 0
for i in range(len(rows)):
    if any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][5]) or any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][11]) or any(x in [7, 8, 9, 10, 11, 12] for x in rows[i][17]):
        num_eudaimonic_motive +=1
#print("People with eudaimonic motives:", num_eudaimonic_motive)

# Computing the average satisfaction (general) amoung users obtaining their motives
count = 0
id_lst = []
sats_lst = []
reg_lst = []
for i in range(len(rows)):
    for j in [6, 12, 18]:
        if all(elem in str(rows[i][j]) for elem in str(rows[i][j-1])) and (len(rows[i][5]) != 0) and (len(rows[i][6]) != 0):
            count += 1
            id_lst.append(rows[i][0])
            sats_lst.append(rows[i][21]) #j+2 for apps sats
            #print(rows[i][0])
            reg_lst.append(rows[i][22])
lst = [i[0] for i in sats_lst if i]
lst2 = [i[0] for i in reg_lst if i]
average = statistics.mean(lst)
average2 = statistics.mean(lst2)
#print("Average satisfaction amoung users obtaining their motives:", average)
#print("Average regret amoung users obtaining their motives:", average2)

#which apps are linked to depression
depression_apps = []
for row in rows:
    app_indices = [7, 13, 19]  # Indices of columns to check for depression
    app_names = [3, 9, 15]     # Indices of cols with app names
    for i in range(len(app_indices)):
        if any(x == 6 for x in row[app_indices[i]]):
            depression_apps.append(row[app_names[i]])
print("Apps reported for depression:", depression_apps)

#which apps are linked to anxiety
anxiety_apps = []
for i in range(len(rows)):
    if any(x in [7] for x in rows[i][7]):
        anxiety_apps.append(rows[i][3])
    if any(x in [7] for x in rows[i][13]):
        anxiety_apps.append(rows[i][9])
    if any(x in [7] for x in rows[i][19]):
        anxiety_apps.append(rows[i][15])
print("Apps reported for anxiety:", anxiety_apps)

#which apps are linked to stress
stress_apps = []
for i in range(len(rows)):
    if any(x in [8] for x in rows[i][7]):
        stress_apps.append(rows[i][3])
    if any(x in [8] for x in rows[i][13]):
        stress_apps.append(rows[i][9])
    if any(x in [8] for x in rows[i][19]):
        stress_apps.append(rows[i][15])
print("Apps reported for stress:", stress_apps)