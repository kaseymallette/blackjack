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

# Create dataframes of 10% and 90% quartiles 
win_quant_03 = shoe_df['win_pct'].quantile(0.03)
win_quant_97 = shoe_df['win_pct'].quantile(0.97)
quant_03_df = shoe_df[shoe_df['win_pct'] < win_quant_03]
quant_97_df = shoe_df[shoe_df['win_pct'] > win_quant_97]

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
sns.displot(data=quant_90_df, x='win_pct', hue='shuffle_method', kde=True,
            multiple='stack')

sns.displot(data=quant_10_df, x='win_pct', hue='shuffle_method', kde=True,
            multiple='stack')

sns.displot(data=shoe_df, x='win_pct', hue='shuffle_method', kde=True,
            multiple='stack')

sns.displot(data=shoe_df, x='win_pct', hue='shuffle_method', kind='kde',
            multiple='stack')

#%%


outlier_high_clumpy = outliers_high_df[outliers_high_df['shuffle_method'] =='riffle_clumpy']
outlier_high_comp = outliers_high_df[outliers_high_df['shuffle_method'] == 'python']
t1 = outlier_high_clumpy['win_pct']
t2 = outlier_high_comp['win_pct']
ttest = stats.ttest_ind(t1,t2)
print("T-Test of outliers with two different shuffles")
print("Python vs riffle clumpy")
print(ttest)

quant_97_clump = quant_97_df[quant_97_df['shuffle_method'] =='riffle_clumpy']
quant_97_py = quant_97_df[quant_97_df['shuffle_method'] == 'python']
t1 = quant_97_clump['win_pct']
t2 = quant_97_py['win_pct']
ttest = stats.ttest_ind(t1,t2)
print("T-Test of outliers with two different shuffles")
print("Quant 95")
print(ttest)