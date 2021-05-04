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

# Rename the index column to hand_index
hand_df = hand_df.rename(columns = {'index': 'hand_index'})

# Iterate through hand_index to identify each shoe
shoe = -1
shoe_index = []
for i in hand_df.index: 
    if hand_df['hand_index'][i] == 0:
        shoe = shoe + 1
    shoe_index.append(shoe)
    
# Add the column shoe_num to hand_df
hand_df.insert(0, 'shoe_index', shoe_index)

# Error 1: Drop rows where player hand = 4 and not [2,2] or [4,14]
error1 = hand_df.loc[hand_df['player'] == '4']


# Error 2: Drop rows where move = 3 instead of is_split = True
error2 = hand_df.loc[hand_df['move'] == '3']

# Error 3: Given a [9,9] against a 7,10,ace, there is an error in the code
error3 = hand_df[(hand_df['player'] == '[9, 9]') 
                & (hand_df['dealer_up'].isin(['7', '10', 'A']))
                & (hand_df['move'] == 'hit')]
    
errors = error1 + error2 + error3
for i in errors.index:
    hand_df = hand_df.drop([i])

#%%
# Find total number of hands and print
total = hand_df['player'].count()
print('\nTotal number of hands: ', total)

# Find number of unique hands
unique_hands = hand_df['player'].value_counts().count()
print('Total number of unique player hands: ', unique_hands)

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
hand_frequency = freq_df('player', 'hand', total, range(0,unique_hands))

# Print top 5 hands
print('\nThe five most frequent player hands:') 
print(hand_frequency.head())

# Print bottom 5 hands
print('\nThe five least frequent player hands:') 
print(hand_frequency.tail())

# Find the frequency of hand outcomes 
outcome_frequency = freq_df('outcome', 'hand outcome', total, range(0,3))
print('\nFrequency of hand outcomes:')
print(outcome_frequency)

# Find the frequency of dealer outcomes
dealer_outcome = freq_df('dealer_outcome', 'dealer outcome', total, range(0,3))
print('\nFrequency of dealer outcomes:')
print(dealer_outcome)

# Find the frequency of player moves
player_moves = freq_df('move', 'player move', total, range(0,3))
print('\nFrequency of player moves: ')
print(player_moves)

# Cound how many hands were split
is_split = hand_df.iloc[:, 9]
split = []

# Create list of is_split
for n in is_split:
    split.append(n)

# Stagger the lists by one element to get x and next 3 elements
split_next = split[1::]
split_next_2 = split[2::]
split_next_3 = split[3::]

# Compare x to y, y to z, and z to w to find num of hands split
count = 0
for x,y,z,w in zip(split, split_next, split_next_2, split_next_3):
    if x is True:
        if x == y:
            if y == z:
                if z == w:
                    count = count + 3
                else:
                    count = count + 2
            else:
                count = count + 1
        else:
            pass
    else:
        pass

# Print number of hands split and percentage of total hands
split_pct = '(' + str(round((count / total * 100), 3)) + '%)'
print('\nNumber of hands split: ', count, split_pct)


#%%
# Define a function to find frequency and avg win of all possible hands
def win_loss_push_pct(player, dealer, move, win, loss, push):
    '''Given empty lists for player, dealer, win, loss, and push, 
    find the frequency of every possible hand combination, 
    in addition to the average win, loss, and push percentage of all 
    possible hands'''
    
    # Find the value counts of all possible hands 
    all_hand_values = hand_df[['player', 'dealer_up']].value_counts()
    
    # To deal with dealer blackjack error, remove hands where frequency < 50
    for i, n in zip(all_hand_values.index, all_hand_values.values):
        if n < 50:
           all_hand_values = all_hand_values.drop(i)
        else:
            # Split the index into two lists and find frequency of hands
            player.append(i[0])
            dealer.append(i[1])
            combo_freq.append(n)
    
    # For each player/dealer combination, remove split hands and dealer bj
    for p, d in zip(player, dealer):
        new_df = hand_df[(hand_df['player'] == p) 
                        & (hand_df['dealer_up'] == d)
                         & (hand_df['is_split'] == False)
                         & (hand_df['dealer_bj'] == False)]

        # Track the basic strategy move for each combination
        row_1 = new_df.iloc[0]
        move.append(row_1['move'])

        # Find the value counts of each outcome and their sum 
        values = new_df['outcome'].value_counts()
        total_count = sum(values)
        
        # Create a dictionary of loss, win, and push percentages
        counts = {}
        for outcome in ['loss', 'push', 'win']:
            if outcome in values.index:
                count = values.loc[outcome]
                count_pct = count/total_count 
                counts[outcome] = round(count_pct, 3)
            else:
                counts[outcome] = 0
        
        # Append the percentages to the empty lists 
        loss.append(counts['loss'])
        win.append(counts['win'])
        push.append(counts['push'])
                   
        
# Create empty lists 
player, dealer, move, win, loss, push, combo_freq = ([] for i in range(7))

# Find avgerages of hand combinations
win_loss_push_pct(player, dealer, move, win, loss, push)

# Create a df that contains columns for player, dealer, and frequency
possible_hands_df = pd.DataFrame({'player': player, 
                               'dealer_up': dealer,
                               'move': move, 
                               'frequency': combo_freq, 
                               'avg_win_pct': win,
                               'avg_loss_pct': loss,
                               'avg_push_pct': push}, 
                               index = range(0, len(player)))



