import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle


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
    train_accuracy = accuracy_score(y_train, model.predict(X_train))
    return model, train_accuracy


def evaluate_model(model, X_test, y_test):
    # Đánh giá mô hình
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    return accuracy, cm, y_test, y_pred


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
        X, y, test_size=0.2, random_state=6)
    model, train_accuracy = train_model(X_train, y_train)
    test_accuracy, cm, y_test, y_pred = evaluate_model(model, X_test, y_test)
    save_model(model, model_filename)
    save_model(vectorizer, vectorizer_filename)
    print(f'Accuracy after update: {test_accuracy}')

    # Lấy danh sách các nhãn
    labels = np.unique(y)

    # Ghi kết quả vào file evaluate.txt
    with open('save_model_SVC/evaluate.txt', 'w') as f:
        f.write(f'Train Accuracy: {train_accuracy}\n')
        f.write(f'Test Accuracy: {test_accuracy}\n')
        f.write(f'Confusion Matrix:\n{cm}\n')
        f.write(f'Labels: {labels.tolist()}\n')


# Cập nhật mô hình với dữ liệu mới
update_model('save_data/classify_duty.csv',
             'save_model_SVC/classify_duty.h5', 'save_model_SVC/count_vectorizer.pkl')
