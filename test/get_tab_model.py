from sklearn.feature_extraction.text import TfidfVectorizer

# Danh sách các chuỗi văn bản
documents = [
    "<bound method BaseWrapper.window_text of <uiawrapper.UIAWrapper - '(9) YouTube - Memory usage - 315 MB', TabItem, 4374795034742144119>>",
    "<bound method BaseWrapper.window_text of <uiawrapper.UIAWrapper - 'regex101: build, test, and debug regex - Memory usage - 105 MB', TabItem, 139478542891626112>>",
    "<bound method BaseWrapper.window_text of <uiawrapper.UIAWrapper - 'ChatGPT - Memory usage - 193 MB', TabItem, -505019471101073820>>",
    "<bound method BaseWrapper.window_text of <uiawrapper.UIAWrapper - 'youtube google - Tìm trên Google', TabItem, 5052624009627132120>>",
    # Thêm nhiều chuỗi văn bản khác nếu có
]

# Tính toán TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

# Trích xuất từ khóa riêng biệt cho mỗi câu
terms = vectorizer.get_feature_names_out()

for i, doc in enumerate(documents):
    print(f"Document {i}:")
    tfidf_scores = X[i].toarray()[0]
    # Sắp xếp các chỉ số theo thứ tự giảm dần của trọng số TF-IDF
    sorted_indices = tfidf_scores.argsort()[::-1]
    # Chọn ra các từ khóa có trọng số TF-IDF lớn nhất và không âm
    top_terms = [terms[idx]
                 for idx in sorted_indices if tfidf_scores[idx] > 0][:10]
    print(f" Top keywords: {top_terms}")
