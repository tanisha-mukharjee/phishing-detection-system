# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
from app.feature_extraction import extract_features
from tqdm import tqdm
import os

print("📥 Loading phishing dataset...")

# Try to detect which dataset is present
dataset_path = None
for filename in os.listdir("dataset"):
    if filename.endswith(".csv"):
        dataset_path = os.path.join("dataset", filename)
        break

if not dataset_path:
    raise FileNotFoundError("❌ No CSV file found inside /dataset folder!")

print(f"✅ Found dataset: {dataset_path}")

# Load dataset
df_raw = pd.read_csv(dataset_path)
print(f"Total URLs loaded: {len(df_raw)}")

# Adjust column names based on dataset type
if 'URL' in df_raw.columns:
    url_col = 'URL'
elif 'url' in df_raw.columns:
    url_col = 'url'
else:
    raise ValueError("❌ No URL column found in the dataset.")

if 'Label' in df_raw.columns:
    label_col = 'Label'
elif 'label' in df_raw.columns:
    label_col = 'label'
elif 'Result' in df_raw.columns:
    label_col = 'Result'
elif 'status' in df_raw.columns:
    label_col = 'status'
elif 'target' in df_raw.columns:
    label_col = 'target'
else:
    print("⚠️ Available columns are:", df_raw.columns)
    raise ValueError("❌ Could not automatically detect the label column. Please check dataset headers.")


# Sample smaller subset if large
df_raw = df_raw.sample(5000, random_state=42)

print("⚙️ Extracting features from URLs...")
data, labels = [], []

for _, row in tqdm(df_raw.iterrows(), total=len(df_raw)):
    url = row[url_col]
    label = 1 if row[label_col].lower() in ['bad', 'phishing', 'malicious'] else 0
    features = extract_features(url)
    data.append(features)
    labels.append(label)

X = pd.DataFrame(data)
y = pd.Series(labels)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
print("🤖 Training phishing detection model...")
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model trained successfully with Accuracy: {accuracy:.2f}")

# Save model
joblib.dump(model, "app/model/phishing_model.pkl")
print("💾 Model saved at app/model/phishing_model.pkl")

with open("app/model/accuracy.txt", "w") as f:
    f.write(str(round(accuracy * 100, 2)))
