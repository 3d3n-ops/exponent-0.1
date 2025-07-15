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
subscription_churn = df.groupby('subscription_type')['churned'].mean() * 100
subscription_churn.plot(kind='bar')
plt.title('Churn Rate by Subscription Type', pad=20)
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=45)

# 2. Watch Hours Distribution for Churned vs Non-Churned
plt.subplot(2, 2, 2)
sns.boxplot(x='churned', y='watch_hours', data=df)
plt.title('Watch Hours Distribution by Churn Status', pad=20)
plt.ylabel('Watch Hours')
plt.xlabel('Churned (0=No, 1=Yes)')

# 3. Last Login Days vs Churn
plt.subplot(2, 2, 3)
sns.boxplot(x='churned', y='last_login_days', data=df)
plt.title('Last Login Days by Churn Status', pad=20)
plt.ylabel('Days Since Last Login')
plt.xlabel('Churned (0=No, 1=Yes)')

# 4. Churn Rate by Payment Method
plt.subplot(2, 2, 4)
payment_churn = df.groupby('payment_method')['churned'].mean() * 100
payment_churn.plot(kind='bar')
plt.title('Churn Rate by Payment Method', pad=20)
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=45)

plt.tight_layout()

# Additional analysis plots
plt.figure(figsize=(20, 10))

# 5. Age Distribution for Churned vs Non-Churned
plt.subplot(1, 2, 1)
sns.kdeplot(data=df[df['churned']==0], x='age', label='Not Churned')
sns.kdeplot(data=df[df['churned']==1], x='age', label='Churned')
plt.title('Age Distribution by Churn Status', pad=20)
plt.xlabel('Age')
plt.ylabel('Density')
plt.legend()

# 6. Watch Time vs Profiles Correlation
plt.subplot(1, 2, 2)
sns.scatterplot(data=df, x='avg_watch_time_per_day', 
                y='number_of_profiles', hue='churned', 
                alpha=0.5)
plt.title('Watch Time vs Number of Profiles', pad=20)
plt.xlabel('Average Watch Time per Day')
plt.ylabel('Number of Profiles')

plt.tight_layout()

# Print key statistics
print("\nChurn Analysis Results:")
print(f"Overall Churn Rate: {df['churned'].mean()*100:.2f}%")
print("\nAverage Watch Hours:")
print(f"Non-churned customers: {df[df['churned']==0]['watch_hours'].mean():.2f}")
print(f"Churned customers: {df[df['churned']==1]['watch_hours'].mean():.2f}")

# Calculate correlation with churn
numerical_cols = ['age', 'watch_hours', 'last_login_days', 
                 'monthly_fee', 'number_of_profiles', 
                 'avg_watch_time_per_day']
correlations = df[numerical_cols].corrwith(df['churned'])
print("\nCorrelations with Churn:")
print(correlations.sort_values(ascending=False))

# Save the final figure
plt.savefig('dataset_analysis.png', dpi=300, bbox_inches='tight')
plt.close('all')