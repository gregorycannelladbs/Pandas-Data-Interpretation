# -*- coding: utf-8 -*-
"""
Created on Sat May  2 15:35:07 2020

@author: Greg
"""
# Github repository URL : https://github.com/gregorycannelladbs/Pandas-Data-Interpretation

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def print_title(title):
    print('#'*80)
    print(title)
    print('#'*80)
    print()
    
plt.close('all')

df = pd.read_csv('survey_results_public.csv')

# Only keep variables of interest
df = df[['Employment','Country', 'EdLevel', 'DevType', 'YearsCode', 
         'YearsCodePro', 'CareerSat', 'ConvertedComp', 'LanguageWorkedWith', 
         'LanguageDesireNextYear','Age']]

# Replace strings values to numerical equivalent
df['YearsCode'].str.replace('Less than 1 year', '0')
df['YearsCodePro'].str.replace('Less than 1 year', '0')
df['YearsCode'].str.replace('More than 50 years', '50')
df['YearsCodePro'].str.replace('More than 50 years', '50')

# Convert strings to numeric values
df['YearsCode'] = pd.to_numeric(df['YearsCode'], errors='coerce')
df['YearsCodePro'] = pd.to_numeric(df['YearsCodePro'], errors='coerce')

# Shorten string values for Employment variable
df['Employment'] = df['Employment'].str.replace('^.*Independent.*$', 'Independent/Freelancer/Self-employed', regex = True)

# Shorten string values for EdLevel variable
df['EdLevel'] = df['EdLevel'].str.replace("^.*Bachelor.*$", "Bachelor", regex = True)
df['EdLevel'] = df['EdLevel'].str.replace("^.*Master.*$", "Master", regex = True)
df['EdLevel'] = df['EdLevel'].str.replace("^.*Associate.*$", "Associate", regex = True)
df['EdLevel'] = df['EdLevel'].str.replace("^.*I never completed.*$", "No high edu", regex = True)
df['EdLevel'] = df['EdLevel'].str.replace("^.*doctoral degree.*$", "PHD", regex = True)
df['EdLevel'] = df['EdLevel'].str.replace("^.*Primary.*$", "No high edu", regex = True)
df['EdLevel'] = df['EdLevel'].str.replace("^.*Professional.*$", "Pro", regex = True)
df['EdLevel'] = df['EdLevel'].str.replace("^.*Secondary.*$", "No high edu", regex = True)
df['EdLevel'] = df['EdLevel'].str.replace("^.*Some college.*$", "Some", regex = True)

df['Employment'].value_counts()
df = df.rename(columns={'ConvertedComp': 'SalaryUSD'})

# Filters to be used
ie_fr = df[df['Country'].isin(['Ireland', 'France'])]
ie = ie_fr[ie_fr['Country'] == 'Ireland']
fr = ie_fr[ie_fr['Country'] == 'France']
real_salaries = ie_fr['SalaryUSD'] < 200000

# Boxplot salary distribution per employment type (France vs Ireland)  
Employment_order = ['Employed part-time', 'Employed full-time', 'Independent/Freelancer/Self-employed']
a = sns.FacetGrid(ie_fr[real_salaries], col='Country', height=6)
a.map_dataframe(sns.boxplot,'Employment', 'SalaryUSD', hue='Employment', dodge=False,
                order=Employment_order, hue_order=Employment_order)
plt.show()

# Percentage of Respondents who work with Python or R (France vs Ireland)
ie_fr_grp = ie_fr.groupby(['Country'])

respondents = ie_fr_grp['LanguageWorkedWith'].count()
python_users = ie_fr_grp['LanguageWorkedWith'].apply(lambda x: x.str.contains('Python').sum())
r_users = ie_fr_grp['LanguageWorkedWith'].apply(lambda x: x.str.contains(';R;').sum())

python_r_df = pd.concat([respondents, python_users, r_users], axis='columns', sort=False)
python_r_df.columns = ['Respondents', 'Python_users', 'R_users']
python_r_df['PctUsesPython'] = python_r_df['Python_users'] / python_r_df['Respondents']
python_r_df['PctUsesR'] = python_r_df['R_users'] / python_r_df['Respondents']

print_title('## Percentage of Respondents who work with Python or R (France vs Ireland)')
print(python_r_df)
print()

# Barplot of Education Level (France vs Ireland)
educ_order = ['No high edu', 'Some', 'Pro', 'Associate', 'Bachelor', 'Master', 'PHD']
fig, ax =plt.subplots(1,2)
edu_ie = test = ie['EdLevel'].value_counts(normalize=True)
edu_fr = test = fr['EdLevel'].value_counts(normalize=True)
sns.barplot(edu_fr.index, edu_fr.values, ax=ax[0], order = educ_order, hue_order = educ_order).set(title='France', ylim=(0, 0.65))
sns.barplot(edu_ie.index, edu_ie.values, ax=ax[1], order = educ_order, hue_order = educ_order).set(title='Ireland', ylim=(0, 0.65))
plt.show()

# Boxplot age distribution (France vs Ireland)
real_ages = ie_fr['Age'] > 16
a = sns.FacetGrid(ie_fr[real_ages], col='Country')
a.map_dataframe(sns.boxplot,'Age', orient='v')
plt.show()

# Pivot table median salary by age (France vs Ireland)
pivot = pd.pivot_table(ie_fr[real_salaries], index='Age', values='SalaryUSD', columns='Country', aggfunc=np.median)

print_title('## Pivot table median salary by age (France vs Ireland)')
print(pivot)
print()

# Pivot table median salary by education level (France vs Ireland)
pivot = pd.pivot_table(ie_fr[real_salaries], index='EdLevel', values='SalaryUSD', columns='Country', aggfunc=np.median)

print_title('## Pivot table median salary by education level (France vs Ireland)')
print(pivot)
print()

# Career satisfaction by education level (France vs Ireland)
satisfaction_grp = ie_fr.groupby(['Country', 'EdLevel'])['CareerSat'].value_counts(normalize=True)

print_title('## Career satisfaction by education level (France vs Ireland)')
print(satisfaction_grp.unstack())