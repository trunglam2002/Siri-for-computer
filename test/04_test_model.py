import pickle

# Tải mô hình đã lưu từ tệp
with open('save_model_SVC/classify_duty.h5', 'rb') as file:
    loaded_model = pickle.load(file)

with open('save_model_SVC/count_vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

# Dữ liệu mới
new_data = ['write to notepad I like bread']

# Chuyển đổi văn bản thành đặc trưng số
new_data_transformed = vectorizer.transform(new_data)

# Dự đoán nhãn
prediction = loaded_model.predict(new_data_transformed)
print(f'Predicted label: {prediction[0]}')
