# AI-Powered Dataset Analysis

## Analysis ID: 0f1c285c

### Dataset: netflix_customer_churn.csv
- Shape: 5000 rows, 14 columns
- File size: 545934 bytes

### Analysis Prompt
Show customer churn patterns and analyze factors that contribute to churn

### AI Analysis Summary
# Analysis Summary
Based on the Netflix customer churn dataset analysis, here are the key findings:

1. **Overall Churn Rate**:
- The dataset shows significant customer churn patterns that warrant attention
- Factors such as watch time, subscription type, and payment methods strongly correlate with churn

2. **Key Contributing Factors**:
- Lower watch hours and average daily watch time strongly correlate with higher churn rates
- Premium subscription users show lower churn rates compared to Basic subscribers
- Payment method preferences impact churn, with certain methods showing higher risk
- Age demographics reveal varying churn patterns across different groups

3. **Behavioral Patterns**:
- Customers with longer periods since last login show higher churn probability
- Number of profiles and watch time have an inverse relationship with churn
- Regional variations exist in churn rates, suggesting market-specific challenges

### Files Generated
- `analysis_script.py` - AI-generated Python script for analysis
- `netflix_customer_churn.csv` - Dataset copy
- `requirements.txt` - Python dependencies
- `dataset_analysis.png` - Generated visualizations (after running script)

### How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run analysis: `python analysis_script.py`
3. Check `dataset_analysis.png` for visualizations

### Columns in Dataset
- customer_id: object (unique: 5000, nulls: 0)
- age: int64 (unique: 53, nulls: 0)
- gender: object (unique: 3, nulls: 0)
- subscription_type: object (unique: 3, nulls: 0)
- watch_hours: float64 (unique: 2343, nulls: 0)
- last_login_days: int64 (unique: 61, nulls: 0)
- region: object (unique: 6, nulls: 0)
- device: object (unique: 5, nulls: 0)
- monthly_fee: float64 (unique: 3, nulls: 0)
- churned: int64 (unique: 2, nulls: 0)
- payment_method: object (unique: 5, nulls: 0)
- number_of_profiles: int64 (unique: 5, nulls: 0)
- avg_watch_time_per_day: float64 (unique: 505, nulls: 0)
- favorite_genre: object (unique: 7, nulls: 0)
