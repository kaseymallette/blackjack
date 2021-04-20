"""
Title: EDA and Regression Model of Shoe Data
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
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures


#%%
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

# Create a column for player count
player_count = round((shoe_df.iloc[:, 0] - shoe_df.iloc[:, 1]), 3)
shoe_df.insert(3, 'player_count', player_count)


#%%
# Describe shoe_df
print('-Descriptive Statsistics-')

# Find the average number of hands per shoe
avg_num_of_hands = round(shoe_df['total_hands'].mean(), 1)
print('\nAverage number of hands per shoe: ')
print(avg_num_of_hands, "hands")

# Describe player win
print('\nPlayer win')
print(shoe_df['player_win'].describe())

# Describe player loss
print('\nPlayer loss')
print(shoe_df['player_loss'].describe())

# Describe push
print('\nHands pushed')
print(shoe_df['push'].describe())

# Describe win percentage
print('\nWin percentage')
print(shoe_df['win_pct'].describe())

# Describe win push percentage
print('\nWin and push percentage')
print(shoe_df['win_push_pct'].describe())


#%%
# Standardize the data
X = shoe_df[['win_pct']]
scaler = preprocessing.RobustScaler().fit(X)
scaled_data = scaler.transform(X)

# Create column of the different shuffles
python_shuffle = shoe_df.loc[shoe_df['shuffle_method'] == 'python']
riffle_perfect = shoe_df.loc[shoe_df['shuffle_method'] == 'riffle_perfect']
riffle_clumpy = shoe_df.loc[shoe_df['shuffle_method'] == 'riffle_clumpy']

# Create column of winning, losing, and even shoes
shoe_df.loc[shoe_df['player_win'] > shoe_df['player_loss'], 'shoe_outcome'] = 'win'
shoe_df.loc[shoe_df['player_win'] < shoe_df['player_loss'], 'shoe_outcome'] = 'loss'
shoe_df.loc[shoe_df['player_win'] == shoe_df['player_loss'], 'shoe_outcome'] = 'even'


#%%
# Define a function to change grid of plots
def change_grid(ax):
    ax.set_facecolor('white')
    ax.grid(which='major', linewidth='0.2', color='gray')
    

# Create distribution plot and histogram of win_pct
fig, (ax1, ax2)  = plt.subplots(1, 2, figsize=(10,5))
change_grid(ax1)
change_grid(ax2)

# Figure 1: Plot the standardized win_pct
ax1.plot(scaled_data,
         c='coral',
         alpha=0.8)

# Set title and xlabel
ax1.set_title('Standardized win percentage', fontsize=12)
ax1.set_xlabel('Number of shoes')

# Figure 2: Histogram of win_pct
n_bins = 16
x = shoe_df['win_pct']

# Use ax.hist to plot n, bins, and patches
n, bins, patches = ax2.hist(x, bins=n_bins)

# Color code the histogram by height and normalize
fracs = n/n.max()
norm = mpl.colors.Normalize(fracs.min(), fracs.max())

# Set the color of each patch
for frac, patch in zip(fracs, patches):
    color = plt.cm.viridis(norm(frac))
    patch.set_facecolor(color)

# Plot the histogram
ax2.hist(x, bins=n_bins, density=True)

# Add title and labels
ax2.set_title('Distribution of Win Percentage', fontsize=12)
ax2.set_ylabel('Number of Shoes')
ax2.set_xlabel('Win Percentage')

# Save figure
plt.savefig('win_pct_hist.png', dpi=300, bbox_inches='tight')

# Create subplot of boxplots of win_pct and with separate shuffles
fig, (ax3, ax4) = plt.subplots(1,2, figsize=(10,5))
change_grid(ax3)
change_grid(ax4)

# Figure 3: Boxplot of win_pct
orange_square = dict(markerfacecolor='tab:orange', marker='s')
ax3.boxplot(shoe_df['win_pct'],
            flierprops = orange_square)

# Set title and labels
ax3.set_title('Win percentage', fontsize=12)
ax3.set_xlabel('All shoes')
ax3.set_ylabel('Win percentage')

# Figure 4: Boxplot of win_pct with different shuffles
boxplot_1 = python_shuffle['win_pct']
boxplot_2 = riffle_perfect['win_pct']
boxplot_3 = riffle_clumpy['win_pct']
data = [boxplot_1, boxplot_2, boxplot_3]
labels = ['python', 'riffle_perfect', 'riffle_clumpy']

# Create boxplot
diamond = dict(markerfacecolor='orchid', marker='d')
boxplot = ax4.boxplot(data,
                      labels=labels,
                      notch=True,
                      patch_artist = True,
                      flierprops = diamond)

# Set title, ylabel, and colors
ax4.set_title('Win percentage with different shuffles', fontsize=12)
ax4.set_ylabel('Win percentage')
colors = ['hotpink', 'deepskyblue', 'palegreen']
for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)

# Save figure
plt.savefig('win_pct_box.png', dpi=300, bbox_inches='tight')

# Show figures
plt.show()


#%%
# Create a probability function 
def find_prob(var, point, description=None, dist=None, two_events=None):
    'Uses a probability density function to find the probability of an event'

    x = shoe_df[var]
    p = stats.norm(loc=x.mean(), scale=x.std())

    # If dist is False, e = 1 - p, otherwise e = p
    if dist == False:
        e = (1 - p.cdf(point))*100
    else:
        e = (p.cdf(point))*100

    # Return e as a floating point
    if two_events == True:
        return e
    # Otherwise, print the event probability as a string
    else:
        event_prob = str(round(e, 1)) + '%'
        print('\n' + description, event_prob)


# Probability
print('\n-Probability-')

# Find mean value of hands pushed
push_mean = round(shoe_df['push'].mean(), 3)
print('\nThe mean value of hands pushed is: ', push_mean)

# Define a good shoe
print('\nDefine a good shoe as: ')
print('A player wins more hands than the dealer and pushes less than 4 times')

# Find the probability of a winning shoe
find_prob('player_count', 1, 'The probability of winning more hands than losing is: ', dist=False)

# Find the probability of pushing at most 4 times
find_prob('push', push_mean, 'The probabilty of pushing at most 3.906 times is: ')

# Find the probability of a good shoe
e1 = find_prob('player_count', 1, dist=False, two_events=True)
e2 = find_prob('push', 3.906, two_events=True)
event = e1*e2/100
event_str = str(round(event, 1)) + '%'
print('\nThe probability of a good shoe is: ', event_str, '\n')


#%%
# Create a dataframe of the winning shoes with low push
win_push_low = shoe_df[(shoe_df['player_count'] >= 1) & (shoe_df['push'] < 4)]

# Create a dataframe of the winning shoes with high push 
win_push_high = shoe_df[(shoe_df['player_count'] >= 1) & (shoe_df['push'] >= 4)]

# Run a ttest comparing means of player_win between low push and high push
low_push = win_push_low['player_win']
high_push = win_push_high['player_win']
ttest = stats.ttest_ind(low_push, high_push)

# Define the two groups 
print('\nRun a ttest comparing means of player win between two groups')
print('Group 1: Player won more hands than dealer and pushed less than 4 times')
print('Group 2: Player won more hands than dealer and pushed more than 4 times\n')

# Print ttest results
print(ttest, '\n')
print('Group 1 mean: ', round(low_push.mean(), 3), ', count: ', len(low_push))
print('Group 2 mean: ', round(high_push.mean(), 3), ', count: ', len(high_push))

# Create plot for hands pushed vs hands won
fig, ax = plt.subplots(figsize=(8,5))
ax.set_ylabel('Hands won')
ax.set_xlabel('Hands pushed')
ax.set_title('Hands pushed vs hands won in winning shoes', fontsize=12)
change_grid(ax)

# Set ymin and ymax
ymin = high_push.min()
ymax = low_push.max()

# Set xmin and xmax
xmin = win_push_low['push'].min()
xmax = win_push_high['push'].max()

# Use fill_between to show both groups 
ax.fill_between((xmin, push_mean), y1=ymin, y2=ymax, facecolor='red', 
                alpha=0.2, label='low push')
ax.fill_between((push_mean, xmax), y1=ymin, y2=ymax, facecolor='blue', alpha=0.2)

# Plot push vs player win in win_push_low and win_push_high
ax.legend([plt.scatter(x=win_push_low['push'], y=win_push_low['player_win']), 
            plt.scatter(x=win_push_high['push'], y=win_push_high['player_win']), 
            plt.vlines(x=3.906, ymin=ymin, ymax=ymax, colors='blue', linestyles='dashed')], 
        ['low push', 'high push', 'x = 3.906'])


# Save figure
plt.savefig('winning_shoes.png', dpi=300, bbox_inches='tight')

# Show plot
plt.show()


#%%
# Define kde function 
def plot_kde(x, ax, xlabel, title):
    'Creates subplots of kernel density estimations'

    data = shoe_df[x]
    loc = data.mean()
    scale = data.std()
    pdf = stats.norm.pdf(data, loc=loc, scale=scale)

    # Plot pdf as a kde
    ax = sns.kdeplot(x=data, y=pdf,fill=True, cmap='coolwarm', ax=ax)

    # Change face color and grid lines
    change_grid(ax)

    # Set title, x and y labels
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Probability Density')


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize=(15,12))
fig.suptitle('Kernel Density Estimations', fontsize=18)

plot_kde('player_win', ax1, 'Hands won', 'KDE of Hands Won')
plot_kde('player_loss', ax2, 'Hands lost', 'KDE of Hands Lost')
plot_kde('push', ax3, 'Hands pushed', 'KDE of Hands Pushed')
plot_kde('player_count', ax4, 'Player count', 'KDE of Player Count')

# Save figure
plt.savefig('kde.png', dpi=300, bbox_inches='tight')

# Show plot
plt.show()


#%%
# Check correlation coefficient and p-value of variables
check_var = ['push', 'doubles_won', 'player_bj', 'dealer_bj',
             'dealer_high_card','dealer_low_card', 'dealer_bust',
             'dealer_stand', 'dealer_draw', 'dealer_avg_hand',
             'num_of_shuffles']

# Print results
print('\n-Correlations-')
print('\nCorrelation coefficients and p-values of variables and win percentage: ')
for var in check_var:
    corr = shoe_df[['player_win', var]].corr()
    pearson_coef, p_value = stats.pearsonr(shoe_df[var], shoe_df['player_win'])
    print('\n', corr)
    print('p = ', p_value)


#%%

# Define plot function against win 
def win_plot(x, color, ax):
    'Plots features against player_win using a lineplot'
    
    # Change face color and grid lines
    change_grid(ax)
    
        
    # Plot a lineplot of x vs player_win
    ax = sns.lineplot(data=shoe_df, x=x, y='player_win', 
                      color = color, ax=ax)


# Create subplots of dealer_bust, dealer_stand, dealer_draw, and push
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, figsize=(5,2))
fig.suptitle('Predicting player win using dealer features', fontsize=18)

# Plot using win_plot
win_plot('dealer_bust', 'orange', ax1)
win_plot('dealer_stand', 'purple', ax2)
win_plot('dealer_draw', 'red', ax3)
win_plot('dealer_high_card', 'blue', ax4)

# Save figure
plt.savefig('dealer_features.png', dpi=100, bbox_inches='tight')

# Create subplots of push and player_bj 
fig, (ax5, ax6) = plt.subplots(2, 1, figsize=(15, 10))
fig.suptitle('Predicting player win using player features', fontsize=18)
win_plot('push', 'green', ax5)
win_plot('player_bj', 'deepskyblue', ax6)

# Save figure
plt.savefig('player_features.png', dpi=300, bbox_inches='tight')

# Show plots
plt.show()


#%%
# Create VIF to check for multicolinarity 
X = shoe_df[['dealer_bust', 'push', 'player_bj']]

# Create VIF dataframe
vif_data = pd.DataFrame()
vif_data['feature'] = X.columns 

# Calculate VIF for each feature
vif_data['VIF'] = [variance_inflation_factor(X.values, i)
                          for i in range(len(X.columns))]

print('\nCheck for multicollinearity using VIF')
print(vif_data)


#%%

# Multiple Linear Regression 

# Define X and y
X = shoe_df[['dealer_bust', 'push', 'player_bj']]
y = shoe_df['player_win']

# Use test_train_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)

# Perform Linear regression 
linreg = LinearRegression().fit(X_train, y_train)

# Print coefficeint, intercept and r-squared for test and train
print('\nMultiple Linear Regression\n')
print('linear model coeff: ', linreg.coef_)
print('linear model intercept: ', round(linreg.intercept_, 3))
print('R-squared score (training): ', round(linreg.score(X_train, y_train), 3))
print('R-squared score (test): ', round(linreg.score(X_test, y_test), 3))

# Perform polynomial regression with degree=3
poly = PolynomialFeatures(degree=3)
X_poly = poly.fit_transform(X)

# Retrain and test the data with X_poly in place of X
X_train, X_test, y_train, y_test = train_test_split(X_poly, y,
                                                   random_state = 0)

# Use ridge regerssion to prevent overfitting
linreg = Ridge().fit(X_train, y_train)

# Print coefficent, intercept, and r-squared for test and train
print('\nPolynomial Regression')
print('(polynomial of degree 3 with ridge regression)\n')
print('linear model coeff: ', linreg.coef_, '\n')
print('linear model intercept: ', round(linreg.intercept_, 3))
print('R-squared score (training): ', round(linreg.score(X_train, y_train), 3))
print('R-squared score (test): ', round(linreg.score(X_test, y_test), 3))

