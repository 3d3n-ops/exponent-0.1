# Example Usage - Dynamic ML Model Generation

This example shows how Exponent-ML generates completely custom code for your specific task and dataset.

## 🎯 Example: Email Spam Classification

### 1. Initialize Project

```bash
exponent init
```

**Interactive prompts:**
```
🧠 Let's set up your ML project!
💬 What task do you want to solve? 
> Predict whether an email is spam or not based on subject and body

📁 Dataset path? 
> spam_dataset.csv

📊 Columns detected: ['subject', 'body', 'label']
📈 Dataset shape: 5000 rows, 3 columns
🤖 Generating code with LLM...
✅ Project created with ID: abc123
```

### 2. Generated Code (No Hard-coded Templates!)

The LLM generates **completely custom code** based on your specific task and dataset:

**`model.py`** - Generated specifically for text classification:
```python
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
import joblib

def preprocess_text(df):
    """Preprocess text data for spam classification."""
    # Combine subject and body
    df['text'] = df['subject'] + ' ' + df['body']
    
    # Clean text
    df['text'] = df['text'].str.lower()
    df['text'] = df['text'].str.replace(r'[^\w\s]', '', regex=True)
    
    return df

def train_spam_classifier(df):
    """Train spam classification model."""
    # Preprocess data
    df = preprocess_text(df)
    
    # Create TF-IDF features
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    X = vectorizer.fit_transform(df['text'])
    y = df['label']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = MultinomialNB()
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    return model, vectorizer, X_test, y_test

# Train the model
model, vectorizer, X_test, y_test = train_spam_classifier(df)
```

**`train.py`** - Generated for your specific dataset:
```python
import pandas as pd
from model import train_spam_classifier
import joblib

# Load dataset
df = pd.read_csv('spam_dataset.csv')

# Train model
model, vectorizer, X_test, y_test = train_spam_classifier(df)

# Save model and vectorizer
joblib.dump(model, 'spam_classifier.joblib')
joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')

print("✅ Model trained and saved!")
```

### 3. Train the Model

```bash
exponent train --project-id abc123 --dataset spam_dataset.csv --task "Predict email spam"
```

The system:
1. ✅ **Loads your generated code** (no hard-coded templates)
2. ✅ **Executes it dynamically** in Modal cloud
3. ✅ **Uses your specific preprocessing** and model choice
4. ✅ **Handles your dataset structure** automatically

### 4. Different Task = Completely Different Code

For a **regression task** with different data:

```bash
exponent init quick "Predict house prices based on square footage and location" --dataset houses.csv
```

**Generated code** (completely different):
```python
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def train_house_price_predictor(df):
    """Train house price prediction model."""
    # Feature engineering
    df['price_per_sqft'] = df['price'] / df['square_footage']
    
    # Select features
    X = df[['square_footage', 'bedrooms', 'bathrooms', 'year_built']]
    y = df['price']
    
    # Train model
    model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    return model, X_test, y_test
```

## 🎯 Key Benefits

✅ **No hard-coded templates** - every model is custom  
✅ **Task-specific preprocessing** - handles your data structure  
✅ **Appropriate model selection** - chooses best algorithm for your task  
✅ **Dynamic feature engineering** - adapts to your dataset  
✅ **Proper evaluation metrics** - classification vs regression  
✅ **Production-ready code** - includes error handling and logging  

The system generates **exactly what you need** for your specific use case! 