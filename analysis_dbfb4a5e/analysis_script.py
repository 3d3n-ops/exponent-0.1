import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Set the style for better visualizations
plt.style.use('seaborn')
sns.set_palette("husl")

# Load the dataset
df = pd.read_csv('netflix_customer_churn.csv')

# Create a figure with multiple subplots
plt.figure(figsize=(20, 15))

# 1. Churn Rate by Subscription Type
plt.subplot(2, 3, 1)
subscription_churn = df.groupby('subscription_type')['churned'].mean() * 100
sns.barplot(x=subscription_churn.index, y=subscription_churn.values)
plt.title('Churn Rate by Subscription Type')
plt.ylabel('Churn Rate (%)')
plt.xlabel('Subscription Type')

# 2. Watch Hours Distribution for Churned vs Non-Churned
plt.subplot(2, 3, 2)
sns.boxplot(x='churned', y='watch_hours', data=df)
plt.title('Watch Hours Distribution by Churn Status')
plt.ylabel('Watch Hours')
plt.xlabel('Churned (1) vs Not Churned (0)')

# 3. Last Login Days vs Churn
plt.subplot(2, 3, 3)
sns.boxplot(x='churned', y='last_login_days', data=df)
plt.title('Last Login Days by Churn Status')
plt.ylabel('Days Since Last Login')
plt.xlabel('Churned (1) vs Not Churned (0)')

# 4. Churn Rate by Payment Method
plt.subplot(2, 3, 4)
payment_churn = df.groupby('payment_method')['churned'].mean() * 100
sns.barplot(x=payment_churn.index, y=payment_churn.values)
plt.title('Churn Rate by Payment Method')
plt.ylabel('Churn Rate (%)')
plt.xlabel('Payment Method')
plt.xticks(rotation=45)

# 5. Average Watch Time vs Churn
plt.subplot(2, 3, 5)
sns.boxplot(x='churned', y='avg_watch_time_per_day', data=df)
plt.title('Average Watch Time by Churn Status')
plt.ylabel('Average Watch Time (hours/day)')
plt.xlabel('Churned (1) vs Not Churned (0)')

# 6. Churn Rate by Region
plt.subplot(2, 3, 6)
region_churn = df.groupby('region')['churned'].mean() * 100
sns.barplot(x=region_churn.index, y=region_churn.values)
plt.title('Churn Rate by Region')
plt.ylabel('Churn Rate (%)')
plt.xlabel('Region')
plt.xticks(rotation=45)

# Adjust layout and save
plt.tight_layout()
plt.savefig('dataset_analysis.png', dpi=300, bbox_inches='tight')

# Print statistical analysis
print("\nChurn Analysis Summary:")
print("-----------------------")
print(f"Overall Churn Rate: {df['churned'].mean()*100:.2f}%")

# Correlation analysis for numerical variables
numerical_cols = ['age', 'watch_hours', 'last_login_days', 'monthly_fee', 
                 'number_of_profiles', 'avg_watch_time_per_day']
correlations = df[numerical_cols + ['churned']].corr()['churned'].sort_values(ascending=False)

print("\nCorrelations with Churn:")
print(correlations)

# Chi-square test for categorical variables
categorical_cols = ['subscription_type', 'gender', 'region', 'device', 'payment_method']
print("\nChi-square Test Results for Categorical Variables:")
for col in categorical_cols:
    chi2, p_value = stats.chi2_contingency(pd.crosstab(df[col], df['churned']))[:2]
    print(f"{col}: chi2={chi2:.2f}, p-value={p_value:.4f}")