import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the style
plt.style.use('default')
sns.set_style('whitegrid')

# Load the dataset
df = pd.read_csv('netflix_customer_churn.csv')

# Create a figure with subplots
plt.figure(figsize=(20, 15))

# 1. Churn Rate by Subscription Type
plt.subplot(2, 2, 1)
subscription_churn = pd.crosstab(df['subscription_type'], df['churned'], normalize='index') * 100
subscription_churn['churned'].plot(kind='bar')
plt.title('Churn Rate by Subscription Type', pad=20)
plt.xlabel('Subscription Type')
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=45)

# 2. Watch Hours Distribution for Churned vs Non-Churned
plt.subplot(2, 2, 2)
sns.boxplot(x='churned', y='watch_hours', data=df)
plt.title('Watch Hours Distribution by Churn Status', pad=20)
plt.xlabel('Churned (0=No, 1=Yes)')
plt.ylabel('Watch Hours')

# 3. Last Login Days vs Churn
plt.subplot(2, 2, 3)
sns.boxplot(x='churned', y='last_login_days', data=df)
plt.title('Last Login Days by Churn Status', pad=20)
plt.xlabel('Churned (0=No, 1=Yes)')
plt.ylabel('Days Since Last Login')

# 4. Churn Rate by Payment Method
plt.subplot(2, 2, 4)
payment_churn = pd.crosstab(df['payment_method'], df['churned'], normalize='index') * 100
payment_churn['churned'].plot(kind='bar')
plt.title('Churn Rate by Payment Method', pad=20)
plt.xlabel('Payment Method')
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=45)

plt.tight_layout()

# Additional analysis
plt.figure(figsize=(20, 8))

# 5. Age Distribution for Churned vs Non-Churned
plt.subplot(1, 2, 1)
sns.kdeplot(data=df[df['churned']==0], x='age', label='Not Churned')
sns.kdeplot(data=df[df['churned']==1], x='age', label='Churned')
plt.title('Age Distribution by Churn Status', pad=20)
plt.xlabel('Age')
plt.ylabel('Density')
plt.legend()

# 6. Average Watch Time vs Churn
plt.subplot(1, 2, 2)
sns.boxplot(x='churned', y='avg_watch_time_per_day', data=df)
plt.title('Average Watch Time per Day by Churn Status', pad=20)
plt.xlabel('Churned (0=No, 1=Yes)')
plt.ylabel('Average Watch Time per Day')

plt.tight_layout()

# Print statistical insights
print("\nChurn Rate Analysis:")
print(f"Overall Churn Rate: {(df['churned'].mean()*100):.2f}%")

print("\nAverage Watch Hours:")
print(df.groupby('churned')['watch_hours'].mean())

print("\nSubscription Type Churn Rates:")
print(subscription_churn['churned'])

# Save the final figure
plt.savefig('dataset_analysis.png', dpi=300, bbox_inches='tight')
plt.close('all')

# Calculate correlation with churn
churn_corr = df.select_dtypes(include=[np.number]).corr()['churned'].sort_values(ascending=False)
print("\nCorrelation with Churn:")
print(churn_corr)