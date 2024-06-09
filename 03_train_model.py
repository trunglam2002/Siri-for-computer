import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pickle

# handle the dataset
# Provide the raw link to the CSV file
url = 'save_data/classify_duty.csv'

# Read the CSV file from the URL
df = pd.read_csv(url)


def generate_X(df):
    X = []
    for line in df['Text']:
        X.append(line)

    return X


def generate_y(df):
    y = []
    for line in df['Intent']:
        y.append(line)

    return y


X_text = generate_X(df)
y_text = generate_y(df)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X_text)
y = np.array(y_text)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Khởi tạo và huấn luyện mô hình
model = SVC()
model.fit(X_train, y_train)

# Lưu CountVectorizer vào một tệp
with open('save_model_SVC/count_vectorizer.pkl', 'wb') as file:
    pickle.dump(vectorizer, file)
print('save model vectorizer sucessful')

# Đánh giá mô hình
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Save the trained model to a file
with open('save_model_SVC/classify_duty.h5', 'wb') as file:
    pickle.dump(model, file)
print('Save model SVC sucessful')
