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
from statsmodels.multivariate.manova import MANOVA
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
print("-Descriptive Statsistics-")

# Find the average number of hands per shoe
avg_num_of_hands = round(shoe_df['total_hands'].mean(), 1)
print("\nAverage number of hands per shoe: ")
print(avg_num_of_hands, "hands")

# Describe player win
print("\nPlayer win")
print(shoe_df['player_win'].describe())

# Describe player loss
print("\nPlayer loss")
print(shoe_df['player_loss'].describe())

# Describe push
print("\nHands pushed")
print(shoe_df['push'].describe())

# Describe win percentage
print("\nWin percentage")
print(shoe_df['win_pct'].describe())

# Describe win push percentage
print("\nWin and push percentage")
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

# Create column of num_of_shuffles
shoe_df.loc[shoe_df['num_of_shuffles'] <= 32 , 'time_of_day'] = 'morning'
shoe_df.loc[(shoe_df['num_of_shuffles'] <= 64) & (shoe_df['num_of_shuffles'] > 32), 'time_of_day'] = 'afternoon'
shoe_df.loc[shoe_df['num_of_shuffles'] > 64, 'time_of_day'] = 'evening'


#%%

# Create distribution plot and histogram of win_pct
fig, (ax1, ax2)  = plt.subplots(1, 2, figsize=(10,5))

# Figure 1: Plot the standardized win_pct
ax1.plot(scaled_data,
         c='coral',
         alpha=0.8)

# Set title and xlabel
ax1.set_title('Standardized win percentage')
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
plt.title('Distribution of Win Percentage')
plt.ylabel('Number of Shoes')
plt.xlabel('Win Percentage')

# Create subplot of boxplots of win_pct and with separate shuffles
fig, (ax3, ax4) = plt.subplots(1,2, figsize=(10,5))

# Figure 3: Boxplot of win_pct
orange_square = dict(markerfacecolor='tab:orange', marker='s')
ax3.boxplot(shoe_df['win_pct'],
            flierprops = orange_square)

# Set title and labels
ax3.set_title('Win percentage')
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
ax4.set_title('Win percentage with different shuffles')
ax4.set_ylabel('Win percentage')
colors = ['hotpink', 'deepskyblue', 'palegreen']
for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)


#%%


def plot_kde(x, ax, xlabel, title):
    'Creates subplots of kernel density estimations'

    data = shoe_df[x]
    loc = data.mean()
    scale = data.std()
    pdf = stats.norm.pdf(data, loc=loc, scale=scale)

    # Plot pdf as a kde
    ax = sns.kdeplot(x=data, y=pdf,fill=True, cmap='coolwarm', ax=ax)

    # Change face color and grid lines
    ax.set_facecolor('white')
    ax.grid(which='major', linewidth='0.2', color='gray')

    # Set title, x and y labels
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Probability Density')


#%%
# Create subplots of probability density function for player_count
fig, ax9 = plt.subplots()
ax9 = sns.lineplot(data=shoe_df, x='player_win', y='dealer_bust', color='orange')
plt.show()

#%%

fig, ((ax5, ax6), (ax7, ax8)) = plt.subplots(2,2, figsize=(15,12))

plot_kde('player_win', ax5, 'Hands won', 'KDE of Hands Won')
plot_kde('player_loss', ax6, 'Hands lost', 'KDE of Hands Lost')
plot_kde('push', ax7, 'Hands pushed', 'KDE of Hands Pushed')
plot_kde('player_count', ax8, 'Player count', 'KDE of Player Count')


#%%

def find_prob(var, point, description=None, dist=None, two_events=None):
    'Uses a probability density function to find the probability of an event'

    x = shoe_df[var]
    p = stats.norm(loc=x.mean(), scale=x.std())

    if dist == False:
        e = (1 - p.cdf(point))*100
    else:
        e = (p.cdf(point))*100

    if two_events == True:
        return e
    else:
        event_prob = str(round(e, 1)) + '%'
        print("\n" + description, event_prob)


# Define a good shoe
print("\n-Probability-")
print("\nDefine a good shoe as: ")
print("A player wins more hands than the dealer and pushes at most 4 times")

# Find the probability of a winning shoe
find_prob('player_count', 1, 'The probability of winning more hands than losing is: ', dist=False)

# Find the probability of pushing at most 4 times
find_prob('push', 4, 'The probabilty of pushing at most 4 times is: ')

# Find the probability of a good shoe
e1 = find_prob('player_count', 1, dist=False, two_events=True)
e2 = find_prob('push', 4, two_events=True)
event = e1*e2/100
event_str = str(round(event, 1)) + '%'
print("\nThe probability of a good shoe is: ", event_str, "\n")

# Create a dataframe of the good shoes
good_shoe_df = shoe_df[(shoe_df['player_count'] >= 1) & (shoe_df['push'] <= 4)]




#%%

# Check correlation coefficient and p-value of variables
check_var = ['push', 'doubles_won', 'player_bj', 'dealer_bj',
             'dealer_high_card','dealer_low_card', 'dealer_bust',
             'dealer_stand', 'dealer_draw', 'dealer_avg_hand',
             'num_of_shuffles', 'player_loss']

# Print results
print("\n-Correlations-")
print("\nCorrelation coefficients and p-values of variables and win percentage: ")
for var in check_var:
    corr = shoe_df[['player_win', var]].corr()
    pearson_coef, p_value = stats.pearsonr(shoe_df[var], shoe_df['player_win'])
    print("\n", corr)
    print("p = ", p_value)



#%%
# Run a MANOVA


maov = MANOVA.from_formula('''shoe_outcome + shuffle_method ~ dealer_bust 
                           + dealer_draw + dealer_stand + time_of_day''',
                           data=shoe_df)
print(maov.mv_test())


#%%

# Create a scatter matrix of dealer_bust, dealer_draw, and dealer_stand
plt.style.use('ggplot')
X = shoe_df[['dealer_bust', 'dealer_draw', 'dealer_stand']]
y = shoe_df['player_win']
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

cmap = mpl.cm.get_cmap('gnuplot')
scatter = pd.plotting.scatter_matrix(X_train, c= y_train, marker = 'o',
                                     s=40, hist_kwds={'bins':15},
                                     figsize=(7,7), diagonal='kde', cmap=cmap)

#%%

# Show plots
plt.show()

#%%

X = shoe_df[['dealer_bust', 'push', 'player_bj']]

# Create VIF dataframe
vif_data = pd.DataFrame()
vif_data['feature'] = X.columns 

# Calculate VIF for each feature
vif_data["VIF"] = [variance_inflation_factor(X.values, i)
                          for i in range(len(X.columns))]

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
print('linear model coeff (w): {}'
     .format(linreg.coef_))
print('linear model intercept (b): {:.3f}'
     .format(linreg.intercept_))
print('R-squared score (training): {:.3f}'
     .format(linreg.score(X_train, y_train)))
print('R-squared score (test): {:.3f}\n'
     .format(linreg.score(X_test, y_test)))

# Perform polynomial regression with degree=3
poly = PolynomialFeatures(degree=3)
X_poly = poly.fit_transform(X)

# Retrain and test the data with X_poly in place of X
X_train, X_test, y_train, y_test = train_test_split(X_poly, y,
                                                   random_state = 0)

# Use ridge regerssion to prevent overfitting
linreg = Ridge().fit(X_train, y_train)

# Print coefficent, intercept, and r-squared for test and train
print('(poly deg 3 + ridge) linear model coeff (w):\n{}'
     .format(linreg.coef_))
print('(poly deg 3 + ridge) linear model intercept (b): {:.3f}'
     .format(linreg.intercept_))
print('(poly deg 3 + ridge) R-squared score (training): {:.3f}'
     .format(linreg.score(X_train, y_train)))
print('(poly deg 3 + ridge) R-squared score (test): {:.3f}'
     .format(linreg.score(X_test, y_test)))

#%%


