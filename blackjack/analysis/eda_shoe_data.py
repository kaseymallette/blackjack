"""
Title: Exploratory Data Analysis of Shoe Data
Author: Kasey Mallette
Created on Tue Mar 23 16:04:48 2021
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
from statsmodels.multivariate.manova import MANOVA


# Load project data
project_dir = 'C:/Users/kcmma/github/blackjack/blackjack/data/'
filename = 'shoe_data.csv'
file_path = Path(project_dir + filename)

# Convert path to Windows format
windows_path = PureWindowsPath(file_path)

# Read csv to dataframe
shoe_df = pd.read_csv(windows_path)

# Drop the index column that contains 0's
shoe_df = shoe_df.drop(['index'], axis=1)

# Create a column for push_pct
player_count = round((shoe_df.iloc[:, 0] - shoe_df.iloc[:, 1]), 3)
shoe_df.insert(3, 'player_count', player_count)

#%%
# Describe shoe_df
describe_df = shoe_df.describe()

# Find the average number of hands per shoe
avg_num_of_hands = round(shoe_df['total_hands'].mean(), 1)
print("\nAverage number of hands per shoe: ", avg_num_of_hands, "hands")

# Find the average percentage of hands won and std
win_pct_mean = shoe_df['win_pct'].mean()
win_pct_std = shoe_df['win_pct'].std()
print("Average win percentage per shoe: ", round(win_pct_mean, 3))

# Find the average number of hands puhsed
push_mean = shoe_df['push'].mean()
print("Average number of hands pushed per shoe: ", round(push_mean, 3))

# Find the average percentage of hands won and pushed
win_push_pct_mean = shoe_df['win_push_pct'].mean()
print("Average win and push percentage per shoe: ", round(win_push_pct_mean, 3))

# Find the min and max of win percentage
win_pct_min = shoe_df['win_pct'].min()
win_pct_max = shoe_df['win_pct'].max()
print("Min win percentage: ", win_pct_min)
print("Max win percentage: ", win_pct_max)

# Standardize the data
X = shoe_df[['win_pct']]
scaler = preprocessing.RobustScaler().fit(X)
scaled_data = scaler.transform(X)
        
# Create dataframes of the different shuffles
python_shuffle = shoe_df.loc[shoe_df['shuffle_method'] == 'python']
riffle_perfect = shoe_df.loc[shoe_df['shuffle_method'] == 'riffle_perfect']
riffle_clumpy = shoe_df.loc[shoe_df['shuffle_method'] == 'riffle_clumpy']

# Create dataframes of winning, losing, and even shoes
shoe_df.loc[shoe_df['player_win'] > shoe_df['player_loss'], 'shoe_outcome'] = 'win'
shoe_df.loc[shoe_df['player_win'] < shoe_df['player_loss'], 'shoe_outcome'] = 'loss'
shoe_df.loc[shoe_df['player_win'] == shoe_df['player_loss'], 'shoe_outcome'] = 'even'

#%%
# Create plots using matplotlib
# Figure 1: Plot the standardized win_pct
fig1, ax1 = plt.subplots()
ax1.plot(scaled_data, 
         c='coral', 
         alpha=0.8)

# Set title and xlabel
ax1.set_title('Standardized win percentage without outliers')
ax1.set_xlabel('Number of shoes')


# Figure 2: Boxplot of win_pct
orange_square = dict(markerfacecolor='tab:orange', marker='s')
fig2, ax2 = plt.subplots()
ax2.boxplot(shoe_df['win_pct'], 
            flierprops = orange_square)

# Set title and labels
ax2.set_title('Win percentage of 2880 shoes')
ax2.set_xlabel('All shoes')
ax2.set_ylabel('Win percentage')


# Figure 3: Boxplot of win_pct with different shuffles 
boxplot_1 = python_shuffle['win_pct']
boxplot_2 = riffle_perfect['win_pct']
boxplot_3 = riffle_clumpy['win_pct']
data = [boxplot_1, boxplot_2, boxplot_3]
labels = ['python', 'riffle_perfect', 'riffle_clumpy']

# Create boxplot
diamond = dict(markerfacecolor='orchid', marker='d')
fig3, ax3 = plt.subplots()
boxplot = ax3.boxplot(data, 
                      labels=labels,
                      notch=True, 
                      patch_artist = True, 
                      flierprops = diamond)

# Set title, ylabel, and colors 
ax3.set_title('Win percentage with different shuffles')
ax3.set_ylabel('Win percentage')
colors = ['hotpink', 'deepskyblue', 'palegreen']
for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)


# Figure 4: Histogram of win_pct
n_bins = 16
x = shoe_df['win_pct']

# Use ax.hist to plot n, bins, and patches
fig4, ax4 = plt.subplots()
n, bins, patches = ax4.hist(x, bins=n_bins)

# Color code the histogram by height and normalize
fracs = n/n.max()
norm = mpl.colors.Normalize(fracs.min(), fracs.max())

# Set the color of each patch
for frac, patch in zip(fracs, patches):
    color = plt.cm.viridis(norm(frac))
    patch.set_facecolor(color)
      
# Plot the histogram
ax4.hist(x, bins=n_bins, density=True)  

# Add title and labels 
plt.title('Distribution of Win Percentage of 2,880 Shoes')
plt.ylabel('Number of Shoes')
plt.xlabel('Win-Push Percentage')


# Figure 5: Plot winning, losing, and even shoes
fig5, ax5 = plt.subplots()

 
# Add title and labels
plt.title('Win percentage of winning, losing, and even shoes')
plt.xlabel('Number of Shoes')
plt.ylabel('Win Percentage')


#%%
# Create probability density function for player_count
pdf_data = shoe_df['player_count']
loc = shoe_df['player_count'].mean()
scale = shoe_df['player_count'].std()
pdf = stats.norm.pdf(pdf_data, loc=loc, scale=scale)

# Figure 6: PDF of win_pct
fig6, ax6 = plt.subplots()
sns.lineplot(x=pdf_data, y=pdf, color='purple', ax=ax6)

# Label plot
plt.title('PDF of Player Count: Hands won minus hands lost')
plt.xlabel('Player count')
plt.ylabel('Probability Density')

# Find probability of winning at least 50% of hands
p = stats.norm(loc=loc, scale=scale)
win_shoe = (1 - p.cdf(0))*100
win_shoe_pct = str(round(win_shoe, 1)) + '%'

# Print probability 
print("\nThe probability of having a winning shoe is:")
print(win_shoe_pct)

# Create probability density function for hands pushed
pdf_data_2 = shoe_df['push']
loc = shoe_df['push'].mean()
scale = shoe_df['push'].std()
pdf_push = stats.norm.pdf(pdf_data_2, loc=loc, scale=scale)

# Figure 7: PDF of hands pushed
fig7, ax7 = plt.subplots()
sns.lineplot(x=shoe_df['push'], y=pdf_push, ax=ax7)

# Label plot
plt.title('PDF of Hands Pushed')
plt.xlabel('Hands Pushed')
plt.ylabel('Probability Density')

# Find probability of pushing 3.9 times 
p2 = stats.norm(loc=loc, scale=scale)
push_below_avg = (p2.cdf(3.9))*100
push_below_avg_pct = str(round(push_below_avg, 1)) + '%'
print("\nThe probability of pushing at most 3.9 hands is:")
print(push_below_avg_pct)

# Create event 
event = win_shoe*push_below_avg/100
event_str = str(round(event, 1)) + '%'
print("\nThe probability of having a winning shoe and pushing at most 3.9 hands is:")
print(event_str)

# Define a good shoe
print("\nDefine a good shoe as: ")
print("A player wins more hands than loses and pushes at most 3.9 hands\n")


#%%
# Show all plots
plt.show()


#%%
# Check correlation coefficient and p-value of variables
check_var = ['push', 'doubles_won', 'player_bj', 'dealer_bj', 
             'dealer_high_card','dealer_low_card', 'dealer_bust', 
             'dealer_stand', 'dealer_draw', 'dealer_avg_hand', 
             'num_of_shuffles']

# Print results
print("\nCorrelation coefficients and p-values of variables and win percentage: ")
for var in check_var:
    corr = shoe_df[['win_pct', var]].corr()
    pearson_coef, p_value = stats.pearsonr(shoe_df[var], shoe_df['win_pct'])
    print("\n", corr)
    print("p = ", p_value)


#%%

# Plot a histogram of dealer_bust
plt.hist(shoe_df['dealer_bust'], bins=16)

# Find counts and bin edges of histogram 
counts, bin_edges = np.histogram(shoe_df['dealer_bust'], bins=16)

# Use counts to create three groups of dealer_bust 
group_1 = counts[0:7].sum()
group_2 = counts[7:9].sum()
group_3 = counts[9:16].sum()

# Use bin edges to create dataframes of dealer_bust
bust_df_low = shoe_df[shoe_df['dealer_bust'] < bin_edges[7]]
bust_df_medium = shoe_df[(shoe_df['dealer_bust'] < bin_edges[9]) & (shoe_df['dealer_bust'] >= bin_edges[7])]
bust_df_high = shoe_df[shoe_df['dealer_bust'] >= bin_edges[9]]

def bust_anova(x, test, test_mean):
    
    a = bust_df_low[x]
    b = bust_df_medium[x]
    c = bust_df_high[x]
    
    anova = stats.f_oneway(a,b,c)
    
    mean_a = a.mean()
    mean_b = b.mean()
    mean_c = c.mean()
    
    print("\n")
    print(test)
    print(anova)
    print("Dealer bust high: ", round(mean_c, 3), test_mean)
    print("Dealer bust medium: ", round(mean_b, 3), test_mean)
    print("Dealer bust low: ", round(mean_a, 3), test_mean)
    
    
# Measure the variance of hands won in three different bust groups    
anova_1 = 'One way anova of player win in three different bust groups'
bust_anova('player_win', anova_1, 'avg hands won')

# Measure the variance of hands pushed in three different bust groups
anova_2 = 'One way anova of hands pushed in three different bust groups'
bust_anova('push', anova_2, 'avg hands pushed')

# Measure the variance of dealer high card in three different bust groups
anova_3 = 'One way anova of dealer high card in three different bust groups'
bust_anova('dealer_high_card', anova_3, 'avg hands with dealer high card')


#%%
# Run a MANOVA

maov = MANOVA.from_formula('shoe_outcome ~ dealer_bust + dealer_draw + dealer_stand',
                           data=shoe_df)
print(maov.mv_test())

