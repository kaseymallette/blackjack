"""
Title: Exploratory Data Analysis of Shoe Data
Author: Kasey Mallette
Created on Tue Mar 23 16:04:48 2021
"""

# Import necessary libraries
import pandas as pd
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


#%%
# Descriptive Statistics
# Find the average number of hands per shoe
avg_num_of_hands = round(shoe_df['total_hands'].mean(), 1)
print("\nAverage number of hands per shoe: ", avg_num_of_hands, "hands")

# Describe win_pct
win_pct_descriptive = shoe_df['win_pct'].describe()
win_pct_mean = shoe_df['win_pct'].mean()
win_pct_std = shoe_df['win_pct'].std()
print("\nDescriptive statsistics for win percentage")
print(win_pct_descriptive)

# Standardize the data
X = shoe_df[['win_pct']]
scaler = preprocessing.RobustScaler().fit(X)
scaled_data = scaler.transform(X)

# Create dataframes of quantiles
win_quant_10 = shoe_df['win_pct'].quantile(0.1)
win_quant_25 = shoe_df['win_pct'].quantile(0.25)
win_quant_50 = shoe_df['win_pct'].quantile(0.5)
win_quant_75 = shoe_df['win_pct'].quantile(0.75)
win_quant_90 = shoe_df['win_pct'].quantile(0.9)
quant_10_df = shoe_df[shoe_df['win_pct'] < win_quant_10]
quant_25_df = shoe_df[shoe_df['win_pct'] < win_quant_25]
quant_50_df = shoe_df[shoe_df['win_pct'] < win_quant_50]
quant_75_df = shoe_df[shoe_df['win_pct'] < win_quant_75]
quant_90_df = shoe_df[shoe_df['win_pct'] > win_quant_90]


# Create dataframes of outliers
std_3 = win_pct_std*3
low = win_pct_mean - std_3
high = win_pct_mean + std_3
outliers_low_df = shoe_df[shoe_df['win_pct'] <= low]
outliers_high_df = shoe_df[shoe_df['win_pct'] >= high]
all_outliers = shoe_df.loc[(shoe_df['win_pct'] < low) | (shoe_df['win_pct'] > high)]


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

# Create a boxplot for win_push_pct of the different shuffles
boxplot_1 = python_shuffle['win_pct']
boxplot_2 = riffle_perfect['win_pct']
boxplot_3 = riffle_clumpy['win_pct']
data = [boxplot_1, boxplot_2, boxplot_3]
labels = ['python', 'riffle_perfect', 'riffle_clumpy']

# Figure 2: Boxplot of win_pct with different shuffles 
fig2, ax2 = plt.subplots()
boxplot = ax2.boxplot(data, 
                      labels=labels,
                      notch=True, 
                      patch_artist = True)

# Set title, ylabel, and colors 
ax2.set_title('Win percentage with different shuffles')
ax2.set_ylabel('Win percentage')
colors = ['pink', 'lightblue', 'lightgreen']
for patch, color in zip(boxplot['boxes'], colors):
        patch.set_facecolor(color)

# Show plots
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
# Use seaborn to create a histogram and kernel density estimate of win_pct

sns.displot(data=shoe_df, x='win_pct', hue='shuffle_method', kde=True,
            multiple='stack')

sns.displot(data=shoe_df, x='win_pct', hue='shuffle_method', kind='kde',
            multiple='stack')

#%%

describe_df = shoe_df.describe()

quant_10_clump = quant_10_df[quant_10_df['shuffle_method'] =='riffle_clumpy']
quant_10_py = quant_10_df[quant_10_df['shuffle_method'] == 'riffle_perfect']
t1 = quant_10_clump['dealer_bust']
t2 = quant_10_py['dealer_bust']
ttest_1 = stats.ttest_ind(t1,t2)
print("T-Test of dealer_bust in 10th quantile of clumpy vs perfect")
print(ttest_1)


