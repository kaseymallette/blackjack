"""
Title: Exploratory Data Analysis of Shoe Data
Author: Kasey Mallette
Created on Tue Mar 23 16:04:48 2021
"""

# Import necessary libraries
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn import preprocessing
from scipy import stats
import seaborn as sns
from pathlib import Path, PureWindowsPath


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



#%%
# Create probability density function for player_count
pdf_data = shoe_df['player_count']
loc = shoe_df['player_count'].mean()
scale = shoe_df['player_count'].std()
pdf = stats.norm.pdf(pdf_data, loc=loc, scale=scale)

# Figure 5: PDF of win_pct
fig5, ax5 = plt.subplots()
sns.lineplot(x=pdf_data, y=pdf, color='purple', ax=ax5)

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

# Figure 6: PDF of hands pushed
fig6, ax6 = plt.subplots()
sns.lineplot(x=shoe_df['push'], y=pdf_push, ax=ax6)

# Label plot
plt.title('PDF of Hands Pushed')
plt.xlabel('Hands Pushed')
plt.ylabel('Probability Density')

# Find probability of pushing at least two hands in a shoe
p2 = stats.norm(loc=loc, scale=scale)
push_4 = (p2.cdf(4))*100
push_4_pct = str(round(push_4, 1)) + '%'
print("\nThe probability of pushing at most four times is:")
print(push_4_pct)

# Create event 
event = win_shoe*push_4/100
event_str = str(round(event, 1)) + '%'
print("\nThe probability of having a winning shoe and pushing 4 times or less is:")
print(event_str)

    
#%%

winning_shoe = shoe_df[shoe_df['player_win'] > shoe_df['player_loss']]
losing_shoe = shoe_df[shoe_df['player_win'] < shoe_df['player_loss']]
even_shoe = shoe_df[shoe_df['player_win'] == shoe_df['player_loss']]

fig7, ax7 = plt.subplots()
plt.plot(winning_shoe['win_pct'])
plt.plot(losing_shoe['win_pct'])
plt.plot(even_shoe['win_pct'])
plt.title('Win percentage of winning, losing, and even shoes')

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
a = python_shuffle['push']
b = riffle_perfect['push']
c = riffle_clumpy['push']
anova_1 = stats.f_oneway(a, b, c)
print("\nOne way anova of different shuffles and hands pushed")
print(anova_1)

a_mean = a.mean()
b_mean = b.mean()
c_mean = c.mean()
print("\nMeans of hands pushed: ")
print("Python shuffle: ", a_mean)
print("Riffle perfect: ", b_mean)
print("Riffle clumpy: ", c_mean)


