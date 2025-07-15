import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Set random seed for reproducibility
np.random.seed(42)

# Load the dataset
df = pd.read_csv('netflix_customer_churn.csv')

# Set the style
plt.style.use('default')
sns.set_style('whitegrid')

# Create a figure with subplots
fig = plt.figure(figsize=(20, 15))
fig.suptitle('Netflix Customer Churn Analysis', fontsize=16, y=0.95)

# 1. Churn Rate by Subscription Type
plt.subplot(2, 3, 1)
churn_by_sub = pd.crosstab(df['subscription_type'], df['churned'], normalize='index') * 100
churn_by_sub['churned'].plot(kind='bar')
plt.title('Churn Rate by Subscription Type')
plt.xlabel('Subscription Type')
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=45)

# 2. Watch Hours Distribution for Churned vs Non-Churned
plt.subplot(2, 3, 2)
sns.boxplot(x='churned', y='watch_hours', data=df)
plt.title('Watch Hours Distribution by Churn Status')
plt.xlabel('Churned (0=No, 1=Yes)')
plt.ylabel('Watch Hours')

# 3. Last Login Days vs Churn
plt.subplot(2, 3, 3)
sns.boxplot(x='churned', y='last_login_days', data=df)
plt.title('Last Login Days by Churn Status')
plt.xlabel('Churned (0=No, 1=Yes)')
plt.ylabel('Days Since Last Login')

# 4. Churn Rate by Payment Method
plt.subplot(2, 3, 4)
churn_by_payment = pd.crosstab(df['payment_method'], df['churned'], normalize='index') * 100
churn_by_payment['churned'].plot(kind='bar')
plt.title('Churn Rate by Payment Method')
plt.xlabel('Payment Method')
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=45)

# 5. Age Distribution for Churned vs Non-Churned
plt.subplot(2, 3, 5)
sns.kdeplot(data=df[df['churned']==0], x='age', label='Not Churned')
sns.kdeplot(data=df[df['churned']==1], x='age', label='Churned')
plt.title('Age Distribution by Churn Status')
plt.xlabel('Age')
plt.ylabel('Density')
plt.legend()

# 6. Correlation Heatmap for Numeric Variables
plt.subplot(2, 3, 6)
numeric_cols = ['age', 'watch_hours', 'last_login_days', 'monthly_fee', 
                'number_of_profiles', 'avg_watch_time_per_day', 'churned']
correlation = df[numeric_cols].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Correlation Heatmap')

# Adjust layout and save
plt.tight_layout()
plt.savefig('dataset_analysis.png', dpi=300, bbox_inches='tight')

# Print key statistics
print("\nChurn Analysis Summary:")
print("-----------------------")
print(f"Overall Churn Rate: {df['churned'].mean()*100:.2f}%")

# Calculate and print statistical significance
for column in ['watch_hours', 'last_login_days', 'age']:
    t_stat, p_val = stats.ttest_ind(
        df[df['churned']==1][column],
        df[df['churned']==0][column]
    )
    print(f"\nStatistical significance for {column}:")
    print(f"t-statistic: {t_stat:.2f}")
    print(f"p-value: {p_val:.4f}")

# Calculate churn rate by subscription type
churn_by_sub = pd.crosstab(df['subscription_type'], df['churned'], normalize='index')
print("\nChurn Rate by Subscription Type:")
print(churn_by_sub['churned'].multiply(100).round(2))

plt.close()