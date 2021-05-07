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
basic_strategy = 'basic_strategy.csv'

# Get file path
file_path = Path(project_dir + filename)
basic_strategy_path = Path(project_dir + basic_strategy)

# Convert path to Windows format
windows_path = PureWindowsPath(file_path)
windows_path_2 = PureWindowsPath(basic_strategy_path)

# Read csv to dataframe
hand_df = pd.read_csv(windows_path)
basic_strategy_df = pd.read_csv(windows_path_2)

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


# Find total number of hands and print
total = hand_df['player'].count()
print('\nTotal number of hands: ', total)

# Find number of unique hands
player_hands = hand_df['player'].value_counts().count()
all_hands = player_hands*10
print('Total number of unique player hands: ', player_hands)
print('Total number of possible player/dealer hand combinations: ', all_hands)

# Find the frequency of unique hands 
hand_frequency = freq_df('player', 'hand', total, range(0,player_hands))

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

# Create a df that contains of all possible hand combinations
possible_hands_df = pd.DataFrame({'player': player, 
                               'dealer_up': dealer,
                               'move': move, 
                               'frequency': combo_freq, 
                               'avg_win_pct': win,
                               'avg_loss_pct': loss,
                               'avg_push_pct': push}, 
                               index = range(0, len(player)))

#%%
# Create two subplots to show the frequency of hands
fig, (ax1, ax2)  = plt.subplots(1, 2, figsize=(13,7))

# Plot a scatter plot of frequency of player hands
hand_frequency = hand_df['player'].value_counts()
hand = hand_frequency.index
ax1.scatter(hand_frequency, hand, c='slateblue')

# Set title and labels for ax1
ax1.set_title('Frequency of unique player hands')
ax1.set_xlabel('Frequency')
ax1.set_ylabel('Player hand')

# Plot a historgram of hand combinations
n_bins = 9
x = possible_hands_df['avg_win_pct']

# Use ax.hist to plot n, bins, and patches
n, bins, patches = ax2.hist(x, bins=n_bins)

# Color code the histogram by height and normalize
fracs = n/n.max()
norm = mpl.colors.Normalize(fracs.min(), fracs.max())

# Set the color of each patch
for frac, patch in zip(fracs, patches):
    color = plt.cm.plasma(norm(frac))
    patch.set_facecolor(color)

# Set title and labels for ax2 
ax2.set_title('Win percentage of unique hand combinations')
ax2.set_xlabel('Win percentage')
ax2.set_ylabel('Number of hands')

# Save figure and show
plt.savefig('images\hand_frequency.png', dpi=100, bbox_inches='tight')
plt.show()


#%%
# Find unique hands excluding splits
unique_hands = possible_hands_df['avg_win_pct'].count()

print('\n---Unique Hand Combinations---')
print('Total number of unique hand combinations excluding splits: ', unique_hands)
print('\nAverage win percentage of unique hand combinations: ')
print(possible_hands_df['avg_win_pct'].describe())

# Find 10th and 90th quantiles 
quant_10 = possible_hands_df['avg_win_pct'].quantile(.10)
quant_90 = possible_hands_df['avg_win_pct'].quantile(.90)

# Create df of hands with a low win percentage
win_pct_low = possible_hands_df[(possible_hands_df['avg_win_pct'] <= quant_10)
                                & (possible_hands_df['move'] == 'hit')]

# Create df of hands with a high win percentage, excluding blackjacks 
win_pct_high = possible_hands_df[(possible_hands_df['avg_win_pct'] < 1)
                              & (possible_hands_df['avg_win_pct'] >= quant_90)]

# Sort values
win_pct_low = win_pct_low.sort_values(by=['player', 'avg_win_pct'])
win_pct_high = win_pct_high.sort_values(by=['player', 'avg_win_pct'])

# Reindex 
win_pct_low = win_pct_low.reset_index()
win_pct_high = win_pct_high.reset_index()

# Drop outliers in win_pct_low and reindex 
win_pct_low = win_pct_low.drop([16,17,18])
win_pct_low = win_pct_low.reset_index()

# Print hands with a low win percentage
print('\nHands with win percentage in or below 10th quantile')
print(win_pct_low.iloc[:, 2:7])

# Print hands with a high win percentage
print('\nHands with win percentage in or above 90th quantile')
print('(Not including blackjack)')
print(win_pct_high.iloc[:, 1:6])


#%%
# Create two subplots to show hands with low and high win pct
fig, (ax1, ax2)  = plt.subplots(1, 2, figsize=(10,6))

# Create a scatter plot of player and dealer hands with low win pct
x1 = win_pct_low['player']
y1 = win_pct_low['dealer_up']
ax1.scatter(x1,y1, c='crimson')

# Set title and labels for ax1
ax1.set_title('Hands with a low win percentage')
ax1.set_xlabel('Player')
ax1.set_ylabel('Dealer')

# Create a scatter plot of player and dealer hands with high win pct
win_pct_high = win_pct_high.sort_values(by=['dealer_up', 'player'], ascending=False)
x2 = win_pct_high['player']
y2 = win_pct_high['dealer_up']
ax2.scatter(x2,y2, c='dodgerblue')

# Set title and labels for ax2 
ax2.set_title('Hands with a high win percentage')
ax2.set_xlabel('Player')
ax2.set_ylabel('Dealer')

# Save figure and show
plt.savefig('images\hand_win_pct.png', dpi=100, bbox_inches='tight')
plt.show()


#%%
# Define a function that updates the rules of basic strategy 
def change_basic_strategy(player, dealer_up, current, new):
    '''Given two lists of player hands and dealer up cards, 
    change the current rule of basic strategy to the new rule'''
    
    for a,b in zip(player, dealer_up):
        # Use a to find the row and index by b to find the value
        row = basic_strategy_df[basic_strategy_df['possible_hands'] == a]
        value = row[b]
        
        # Find the index and value of current 
        index = value.index[0]
        new_value = value.values
        
        # Change current to new
        if b == 'A':
            if new_value == str(current):
                new_value = str(new)
        else: 
            if new_value == current:
                new_value = new
        
        # Update value 
        basic_strategy_df.at[index, b] = new_value
        

# Create two lists for player and dealer 
win_low_player = []
win_low_dealer = []

# Get values from win_pct_low 
for i,j in zip(win_pct_low.player.values, win_pct_low.dealer_up.values):
    win_low_player.append(i)
    win_low_dealer.append(j)

# Change basic strategy for hands with low win percentage
change_basic_strategy(win_low_player, win_low_dealer, 1, 0)

# Export basic strategy changes to csv 
basic_strategy_df.to_csv(project_dir+'basic_strategy_changes.csv', index=False)

