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
from scipy import stats
import seaborn as sns
from pathlib import Path, PureWindowsPath
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree


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

# Drop errors     
errors = error1 + error2 + error3
for i in errors.index:
    hand_df = hand_df.drop([i])
    
# Dummy code bust rate and stagger list by 1
dealer_bust = [0]
for n in hand_df['dealer_outcome'].values:
    if n == 'bust':
        count = 1
    else:
        count = 0
    dealer_bust.append(count)

# Remove last item from list
dealer_bust.pop(-1)

# Insert dummy coded dealer bust 
hand_df.insert(7, 'dealer_bust', dealer_bust)

# Find rolling bust rate for every 5 and 10 hands
bust_rate_5 = (hand_df['dealer_bust']/5).rolling(window=5).sum()
bust_rate_10 = (hand_df['dealer_bust']/10).rolling(window=10).sum()
    
# Insert dealer bust rates 
hand_df.insert(8, 'bust_rate_5', bust_rate_5)
hand_df.insert(9, 'bust_rate_10', bust_rate_10)

# Change NaN values to 0
hand_df['bust_rate_5'] = hand_df['bust_rate_5'].fillna(0)
hand_df['bust_rate_10'] = hand_df['bust_rate_10'].fillna(0)

# For values e-17, change to 0
for i, j, m, n in zip(hand_df['bust_rate_5'].index, 
                      hand_df['bust_rate_10'].index, 
                      hand_df['bust_rate_5'], 
                      hand_df['bust_rate_10']):
    # Add 1 to all values
    if (m+1) == 1.0: 
        hand_df.at[i, 'bust_rate_5'] = 0
    else:
        hand_df.at[i, 'bust_rate_5'] = round(m, 1)
    if (n+1) == 1.0:
        hand_df.at[j, 'bust_rate_10'] = 0
    else:
        hand_df.at[i, 'bust_rate_10'] = round(n, 1)


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
print('\n---Frequencies---')
print('The five most frequent player hands:') 
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
is_split = hand_df.iloc[:, 12]
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

# Run crosstab of bust_rate for last five hands and outcome
crosstab = pd.crosstab(hand_df['bust_rate_5'], hand_df['outcome'])

# Print crosstab
print('\n---Dealer Bust Rate---')
print('Crosstab of bust rate for last five hands and outcome')
print(crosstab)

# Find chi2 of crosstab and print
chi2, p, dof, expected = stats.chi2_contingency(crosstab)
print('\nChi-squared value: ', chi2)
print('p-value: ', p)
print('Degress of freedom: ', dof)
print('\nExpected: ', expected)


#%%
# Define a function to find frequency and avg win of all possible hands
def win_loss_push_pct(df, player, dealer, freq, move, win, loss, push):
    '''Given empty lists for player, dealer, win, loss, and push, 
    find the frequency of every possible hand combination, 
    in addition to the average win, loss, and push percentage of all 
    possible hands'''
    
    # Find the value counts of all possible hands 
    all_hand_values = df[['player', 'dealer_up']].value_counts()
    
    # To deal with dealer blackjack error, remove hands where frequency < 25
    for i, n in zip(all_hand_values.index, all_hand_values.values):
        if n < 40:
           all_hand_values = all_hand_values.drop(i)
        else:
            # Split the index into two lists and find frequency of hands
            player.append(i[0])
            dealer.append(i[1])
            freq.append(n)
    
    # For each player/dealer combination, remove split hands and dealer bj
    for p, d in zip(player, dealer):
        new_df = df[(df['player'] == p) 
                        & (df['dealer_up'] == d)
                         & (df['is_split'] == False)
                         & (df['dealer_bj'] == False)]

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
player, dealer, move, win, loss, push, freq = ([] for i in range(7))

# Find avgerages of hand combinations
win_loss_push_pct(hand_df, player, dealer, freq, move, win, loss, push)

# Create a df that contains of all possible hand combinations
possible_hands = pd.DataFrame({'player': player, 
                               'dealer_up': dealer,
                               'move': move, 
                               'frequency': freq, 
                               'avg_win_pct': win,
                               'avg_loss_pct': loss,
                               'avg_push_pct': push}, 
                               index = range(0, len(player)))


#%%
# Create crosstabs of player and dealer hands and outcome
dealer_crosstab = pd.crosstab(hand_df['dealer_up'], hand_df['outcome'])
player_crosstab = pd.crosstab(hand_df['player'], hand_df['outcome'])
player_crosstab = player_crosstab[2:12]

# Plot crosstabs
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15,11))
ax1 = dealer_crosstab.plot.bar(stacked=True, cmap='flare_r', ax=ax1)
ax2 = player_crosstab.plot.bar(stacked=True, cmap='flare_r', ax=ax2)

# Plot heatmaps of crosstabs
ax3 = sns.heatmap(dealer_crosstab, cmap='rocket_r', annot=True, fmt='g', ax=ax3)
ax4 = sns.heatmap(player_crosstab, cmap='rocket_r', annot=True, fmt='g', ax=ax4)

# Set titles, save, and plot
ax1.set_title('Dealer Up')
ax2.set_title('Player')
plt.savefig('images\hand_outcomes.png', dpi=100, bbox_inches='tight')
plt.show()


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
x = possible_hands['avg_win_pct']

# Use ax.hist to plot n, bins, and patches
n, bins, patches = ax2.hist(x, bins=n_bins)

# Color code the histogram by height and normalize
fracs = n/n.max()
norm = mpl.colors.Normalize(fracs.min(), fracs.max())

# Set the color of each patch
for frac, patch in zip(fracs, patches):
    color = plt.cm.inferno(norm(frac))
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
unique_hands = possible_hands['avg_win_pct'].count()

print('\n---Unique Hand Combinations---')
print('Total number of unique hand combinations excluding splits: ', unique_hands)
print('\nAverage win percentage of unique hand combinations: ')
print(possible_hands['avg_win_pct'].describe())

# Find 10th and 90th quantiles 
quant_10 = possible_hands['avg_win_pct'].quantile(.10)
quant_90 = possible_hands['avg_win_pct'].quantile(.90)

# Create df of hands with a low win percentage
win_pct_low = possible_hands[(possible_hands['avg_win_pct'] <= quant_10)
                                & (possible_hands['move'] == 'hit')]

# Create df of hands with a high win percentage, excluding blackjacks 
win_pct_high = possible_hands[(possible_hands['avg_win_pct'] < 1)
                              & (possible_hands['avg_win_pct'] >= quant_90)]

# Sort values
win_pct_low = win_pct_low.sort_values(by=['player', 'avg_win_pct'])
win_pct_high = win_pct_high.sort_values(by=['player', 'avg_win_pct'])

# Reindex 
win_pct_low = win_pct_low.reset_index()
win_pct_high = win_pct_high.reset_index()

# Drop outliers in win_pct_low and reindex 
win_pct_low = win_pct_low.drop([14, 15, 16, 17])
win_pct_low = win_pct_low.reset_index()
win_pct_low = win_pct_low.drop(columns=['level_0', 'index'])
win_pct_high = win_pct_high.drop(columns=['index'])

# Print hands with a low win percentage
print('\nHands with win percentage in or below 10th quantile')
print(win_pct_low.iloc[:, 0:5])

# Print hands with a high win percentage
print('\nHands with win percentage in or above 90th quantile')
print('(Not including blackjack)')
print(win_pct_high.iloc[:, 0:5])


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


#%%
# Load project data from hand_data_2 and get file path
filename_2 = 'hand_data_2.csv'
file_path_2 = Path(project_dir + filename_2)
if file_path_2.exists() is False:
    print('Error!', filename_2, 'does not exist!')
else:
    # Get path
    windows_path_2 = PureWindowsPath(file_path_2)

    # Read csv to dataframe
    hand_df_2 = pd.read_csv(windows_path_2)

    # Rename the index column to hand_index
    hand_df_2 = hand_df_2.rename(columns = {'Unnamed: 0': 'hand_index'})

    # Iterate through hand_index to identify each shoe
    shoe_2 = -1
    shoe_index_2 = []
    for i in hand_df_2.index: 
        if hand_df_2['hand_index'][i] == 0:
            shoe_2 = shoe_2 + 1
        shoe_index_2.append(shoe)
    
    # Add the column shoe_num to hand_df_2
    hand_df_2.insert(0, 'shoe_index', shoe_index_2)

    # Error 1: Drop rows where player hand = 4 and not [2,2] or [4,14]
    error1 = hand_df_2.loc[hand_df_2['player'] == '4']

    # Error 2: Drop rows where move = 3 instead of is_split = True
    error2 = hand_df_2.loc[hand_df_2['move'] == '3']

    # Drop errors 
    errors = error1 + error2
    for i in errors.index:
        hand_df_2 = hand_df_2.drop([i])
    
    
    # Create empty lists 
    player2, dealer2, move2, win2, loss2, push2, freq2 = ([] for i in range(7))

    # Find avgerages of hand combinations
    win_loss_push_pct(hand_df_2, player2, dealer2, freq2, move2, win2, loss2, push2)

    # Create a df that contains of all possible hand combinations
    possible_hands_2 = pd.DataFrame({'player': player2, 
                                     'dealer_up': dealer2,
                                     'move': move2, 
                                     'frequency': freq2, 
                                     'avg_win_pct': win2,
                                     'avg_loss_pct': loss2,
                                     'avg_push_pct': push2}, 
                                    index = range(0, len(player2)))

    win_low_changes = pd.DataFrame(columns = ['player', 'dealer', 'move', 
                                          'frequency', 'avg_win_pct', 
                                          'avg_loss_pct', 'avg_push_pct'], 
                                   index = range(0, 19))

    index = 0
    for i,j in zip(win_low_player, win_low_dealer):
        add_row = possible_hands_2[(possible_hands_2['player'] == i)
                                       & (possible_hands_2['dealer_up'] == j)]
    
        win_low_changes.loc[index] = add_row.values
        index +=1 
    
    # Change data types 
    win_low_changes['frequency'] = win_low_changes['frequency'].astype(int)
    win_low_changes['avg_win_pct'] = win_low_changes['avg_win_pct'].astype(float)
    win_low_changes['avg_loss_pct'] = win_low_changes['avg_loss_pct'].astype(float)
    win_low_changes['avg_push_pct'] = win_low_changes['avg_push_pct'].astype(float)

    # T-test of avg_win_pct for low win hands and their rule changes
    a = win_pct_low['avg_win_pct']
    b = win_low_changes['avg_win_pct']
    ttest = stats.ttest_ind(a, b)
    print('\n---Playing Against Basic Strategy---')
    print('\nAverage win percentage')
    print('T-test of win percentage of low win hands and their rule changes')
    print(ttest)
    print('Original hands: ', round(a.mean(), 3))
    print('Rule changes: ', round(b.mean(), 3))
    
    # T-test of avg_loss_pct for low win hands and their rule changes
    a2 = win_pct_low['avg_loss_pct']
    b2 = win_low_changes['avg_loss_pct']
    ttest2 = stats.ttest_ind(a2, b2)
    print('\n Average loss percentage')
    print('T-test of loss percentage of low win hands and their rule changes')
    print(ttest2)
    print('Original hands: ', round(a2.mean(), 3))
    print('Rule changes: ', round(b2.mean(), 3), '\n')
    
    
#%%
# Define hard hands
hard_hands = ['8', '9', '10', '11', '12', '13', '14', '15', 
              '16', '17', '18', '19', '20', '21']
    
# Create df of hard hands and replace dealer ace as 11
hard_hands_df = hand_df[hand_df['player'].isin(hard_hands)]
dealer_ace = hard_hands_df['dealer_up'] == 'A'
hard_hands_df.loc[dealer_ace, 'dealer_up'] = 11

# Define X and y
X = hard_hands_df[['player', 'dealer_up']]
y = hard_hands_df['outcome']
    
# Use test_train_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)
    
# Logistic Regression 
logreg = LogisticRegression().fit(X_train, y_train)
print('\n---Predicting hand outcomes---')
print('Using player hand and dealer up to predict outcome of hard hands')
print('\nLogistic Regression')
print('Train score: ', round(logreg.score(X_train, y_train), 3))
print('Test score: ', round(logreg.score(X_test, y_test), 3))

# Decision Tree Classifier 
clf = DecisionTreeClassifier(max_leaf_nodes=15, max_depth=5, random_state=0)
clf.fit(X_train, y_train)
print('\nDecision Tree Classifier')
print('Train score: ', round(clf.score(X_train, y_train), 3))
print('Test score: ', round(clf.score(X_test, y_test), 3))

# Plot Decision Tree
fig, ax = plt.subplots(figsize=(12,7))
ax = tree.plot_tree(clf, ax=ax)
plt.title('Decision Tree Classifier of Hand Outcome')

# Save figure and plot 
plt.savefig('images\decision_tree_classifer.png', dpi=100, bbox_inches='tight')
plt.show()


#%%
# Load project data from good_shoes and get file path
good_shoe_filename = 'good_shoes.csv'
good_shoe_path = Path(project_dir + good_shoe_filename)
if good_shoe_path.exists() is False:
    print('Error!', filename_2, 'does not exist!')
else: 
    # Get path and read csv to dataframe
    good_shoe_windows = PureWindowsPath(good_shoe_path)
    good_shoe_df = pd.read_csv(good_shoe_windows)
    
    # Create dataframe of good shoes for first shoe index
    start = good_shoe_df['shoe_index'].iloc[0]
    good_shoe_hands = hand_df[(hand_df['shoe_index'] == start) & 
                              (hand_df['player'].isin(hard_hands))]
    
    # For each shoe index, add hands 
    for i in good_shoe_df['shoe_index'].iloc[1::]:
        add_hands = hand_df[(hand_df['shoe_index'] == i) & 
                            (hand_df['player'].isin(hard_hands))]
        
        good_shoe_hands = good_shoe_hands.append(add_hands)
    
    # Replace dealer up ace as 11
    dealer_ace = good_shoe_hands['dealer_up'] == 'A'
    good_shoe_hands.loc[dealer_ace, 'dealer_up'] = 11
    
    # Define X and y
    X = good_shoe_hands[['player', 'dealer_up']]
    y = good_shoe_hands['outcome']
    
    # Use test_train_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)
    
    # Logistic Regression 
    logreg = LogisticRegression().fit(X_train, y_train)
    print('\nPredicting outcome of hard hands from good shoes')
    print('\nLogistic Regression')
    print('Train score: ', round(logreg.score(X_train, y_train), 3))
    print('Test score: ', round(logreg.score(X_test, y_test), 3))

    # Decision Tree Classifier
    clf = DecisionTreeClassifier(max_leaf_nodes=15, max_depth=5, random_state=0)
    clf.fit(X_train, y_train)
    print('\nDecision Tree Classifier')
    print('Train score: ', round(clf.score(X_train, y_train), 3))
    print('Test score: ', round(clf.score(X_test, y_test), 3))
    
