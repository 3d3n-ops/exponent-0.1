import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

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
subscription_churn.plot(kind='bar', color=['#2ecc71', '#e74c3c', '#3498db'])
plt.title('Churn Rate by Subscription Type', fontsize=12, pad=15)
plt.xlabel('Subscription Type')
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=45)

# 2. Watch Hours Distribution for Churned vs Non-Churned
plt.subplot(2, 2, 2)
sns.boxplot(x='churned', y='watch_hours', data=df, palette=['#2ecc71', '#e74c3c'])
plt.title('Watch Hours Distribution by Churn Status', fontsize=12, pad=15)
plt.xlabel('Churned (0=No, 1=Yes)')
plt.ylabel('Watch Hours')

# 3. Age Distribution and Churn
plt.subplot(2, 2, 3)
sns.kdeplot(data=df[df['churned']==0], x='age', label='Not Churned', color='#2ecc71')
sns.kdeplot(data=df[df['churned']==1], x='age', label='Churned', color='#e74c3c')
plt.title('Age Distribution by Churn Status', fontsize=12, pad=15)
plt.xlabel('Age')
plt.ylabel('Density')
plt.legend()

# 4. Payment Method and Churn
plt.subplot(2, 2, 4)
payment_churn = df.groupby('payment_method')['churned'].mean() * 100
payment_churn.plot(kind='bar', color=sns.color_palette("husl", len(payment_churn)))
plt.title('Churn Rate by Payment Method', fontsize=12, pad=15)
plt.xlabel('Payment Method')
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=45)

# Adjust layout and save
plt.tight_layout()
plt.savefig('dataset_analysis.png', dpi=300, bbox_inches='tight')

# Print statistical analysis
print("\nChurn Analysis Results:")
print("-----------------------")
print(f"Overall Churn Rate: {df['churned'].mean()*100:.2f}%")

# Correlation analysis
correlations = df[['watch_hours', 'last_login_days', 'monthly_fee', 'number_of_profiles', 'avg_watch_time_per_day', 'churned']].corr()['churned'].sort_values(ascending=False)
print("\nCorrelations with Churn:")
print(correlations)

# Chi-square test for categorical variables
def chi_square_test(df, categorical_var):
    contingency = pd.crosstab(df[categorical_var], df['churned'])
    chi2, p_value = stats.chi2_contingency(contingency)[:2]
    return categorical_var, chi2, p_value

categorical_vars = ['subscription_type', 'payment_method', 'region', 'device']
print("\nChi-square Tests for Categorical Variables:")
for var in categorical_vars:
    var_name, chi2, p_value = chi_square_test(df, var)
    print(f"{var_name}: chi2={chi2:.2f}, p-value={p_value:.4f}")

# Clean up
plt.close()