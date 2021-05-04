"""
Title: Exploratory Data Analysis of Hand Data
Author: Kasey Mallette
Created on Tue Mar 23 16:07:25 2021
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy import stats
import seaborn as sns
from pathlib import Path, PureWindowsPath
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn import metrics


#%%
# Load project data
project_dir = 'C:/Users/kcmma/github/blackjack/blackjack/data/'
filename = 'hand_data.csv'
file_path = Path(project_dir + filename)

# Convert path to Windows format
windows_path = PureWindowsPath(file_path)

# Read csv to dataframe
hand_df = pd.read_csv(windows_path)

# Drop the index column that contains 0's
hand_df = hand_df.rename(columns = {'index': 'hand_index'})

# Iterate through shoe_index to identify each shoe
shoe = -1
shoe_num = []
for i in hand_df.index: 
    if hand_df['hand_index'][i] == 0:
        shoe = shoe + 1
    shoe_num.append(shoe)
    
# Add the column shoe_num to hand_df
hand_df.insert(0, 'shoe_index', shoe_num)


#%%
# Find total number of hands and print
total = hand_df['player'].count()
print('\nTotal number of hands: ', total)

# Find number of unique hands
hand_counts = hand_df['player'].value_counts()
print('Total number of unique player hands: ', hand_counts.count(), '\n')

# Define a function that finds frequency and percentage 
def freq_df(column, event, total, index):
    ''''Given a column in hand_df, define the event, find the frequency
    of each occurance using value_counts(), and the percentage by dividing
    the count of each occurance by the total number of occurrances'''
    
    counts = hand_df[column].value_counts()
    pct = []
    freq = []

    for n in counts:
        freq.append(n)
        p = round((n/total * 100), 3)
        p_str = str(p) + '%'
        pct.append(p_str)
        
    new_df = pd.DataFrame({event: counts.index, 
                           'frequency': freq, 
                           'percentage': pct}, 
                          index = index)
    
    return new_df 



# Find the frequency of unique hands 
hand_frequency = freq_df('player', 'hand', total, range(0,34))
print(hand_frequency)

# Find the frequency of hand outcomes 
outcome_frequency = freq_df('outcome', 'hand outcome', total, range(0,3))
print('\nFrequency of hand outcomes:')
print(outcome_frequency)

# Find the frequency of dealer outcomes
dealer_outcome = freq_df('dealer_outcome', 'dealer outcome', total, range(0,3))
print('\nFrequency of dealer outcomes:')
print(dealer_outcome)
