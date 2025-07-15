import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the style for better visualizations
plt.style.use('seaborn')
sns.set_palette("husl")

# Load the dataset
df = pd.read_csv('netflix_customer_churn.csv')

# Create a figure with multiple subplots
fig = plt.figure(figsize=(20, 15))
fig.suptitle('Netflix Customer Churn Analysis', fontsize=16, y=0.95)

# 1. Churn Rate by Subscription Type
plt.subplot(2, 3, 1)
subscription_churn = df.groupby('subscription_type')['churned'].mean() * 100
subscription_churn.plot(kind='bar')
plt.title('Churn Rate by Subscription Type')
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=45)

# 2. Watch Hours Distribution for Churned vs Non-Churned
plt.subplot(2, 3, 2)
sns.boxplot(x='churned', y='watch_hours', data=df)
plt.title('Watch Hours Distribution by Churn Status')
plt.ylabel('Watch Hours')
plt.xlabel('Churned (1) vs Non-Churned (0)')

# 3. Last Login Days Impact
plt.subplot(2, 3, 3)
sns.boxplot(x='churned', y='last_login_days', data=df)
plt.title('Last Login Days by Churn Status')
plt.ylabel('Days Since Last Login')
plt.xlabel('Churned (1) vs Non-Churned (0)')

# 4. Payment Method Analysis
plt.subplot(2, 3, 4)
payment_churn = df.groupby('payment_method')['churned'].mean() * 100
payment_churn.plot(kind='bar')
plt.title('Churn Rate by Payment Method')
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=45)

# 5. Age Distribution
plt.subplot(2, 3, 5)
sns.kdeplot(data=df, x='age', hue='churned', common_norm=False)
plt.title('Age Distribution by Churn Status')
plt.xlabel('Age')
plt.ylabel('Density')

# 6. Average Watch Time Impact
plt.subplot(2, 3, 6)
sns.scatterplot(data=df, x='avg_watch_time_per_day', y='watch_hours', 
                hue='churned', alpha=0.5)
plt.title('Watch Patterns and Churn')
plt.xlabel('Avg Watch Time per Day')
plt.ylabel('Total Watch Hours')

# Adjust layout and save
plt.tight_layout()
plt.savefig('dataset_analysis.png', dpi=300, bbox_inches='tight')

# Print key statistics
print("\nKey Churn Statistics:")
print(f"Overall Churn Rate: {df['churned'].mean()*100:.2f}%")
print("\nChurn Rate by Subscription Type:")
print(subscription_churn)
print("\nAverage Watch Hours:")
print(f"Churned Customers: {df[df['churned']==1]['watch_hours'].mean():.2f}")
print(f"Non-Churned Customers: {df[df['churned']==0]['watch_hours'].mean():.2f}")

# Correlation analysis for numerical variables
numerical_cols = ['age', 'watch_hours', 'last_login_days', 'monthly_fee', 
                 'number_of_profiles', 'avg_watch_time_per_day']
correlation = df[numerical_cols + ['churned']].corr()['churned'].sort_values()
print("\nCorrelation with Churn:")
print(correlation)

# Close the figure to free memory
plt.close()