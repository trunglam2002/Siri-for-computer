import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import pickle
from sklearn.metrics import confusion_matrix


def load_data(url):
    # Đọc dữ liệu từ file CSV
    df = pd.read_csv(url)
    return df


def preprocess_data(df):
    # Tiền xử lý dữ liệu
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(df['Text'])
    y = np.array(df['Intent'])
    return X, y, vectorizer


def train_model(X_train, y_train):
    # Huấn luyện mô hình
    model = MultinomialNB()
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    # Đánh giá mô hình
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


def save_model(model, filename):
    # Lưu mô hình vào file
    with open(filename, 'wb') as file:
        pickle.dump(model, file)
    print(f'Saved model to {filename}')


def update_model(url, model_filename, vectorizer_filename):
    # Cập nhật mô hình với dữ liệu mới
    df = load_data(url)
    X, y, vectorizer = preprocess_data(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train)
    accuracy = evaluate_model(model, X_test, y_test)
    y_pred = model.predict(X_test)
    print(confusion_matrix(y_test, y_pred))
    save_model(model, model_filename)
    save_model(vectorizer, vectorizer_filename)
    print(f'Accuracy after update: {accuracy}')


# Cập nhật mô hình với dữ liệu mới
update_model('save_data/classify_duty.csv', 'save_model_SVC/classify_duty.h5',
             'save_model_SVC/count_vectorizer.pkl')
