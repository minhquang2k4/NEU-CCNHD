import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer # để chuyển đổi dữ liệu văn bản thành ma trận TF-IDF
from sklearn.metrics.pairwise import cosine_similarity # để tính toán độ tương đồng giữa các mẫu

def load_data(file_path):
  data = pd.read_csv(file_path)
  return data

def preprocess_data(data):
  # Tạo một cột mới có tên là "combined_text" chứa nội dung của các cột "Title", "Author" và "Description"
  data["combined_text"] = data["Title"].fillna('') + ' ' + data["Author"].fillna('') + ' ' + data['Description'].fillna('')
  
  # Tạo đối tượng TfidfVectorizer để chuyển đổi dữ liệu văn bản thành ma trận TF-IDF
  vietnamese_stop_words = ['và', 'là', 'của', 'nhưng', 'nếu', 'bởi', 'vì']
  tfidf_vectorizer = TfidfVectorizer(stop_words=vietnamese_stop_words)
  
  # Chuyển đổi dữ liệu văn bản thành ma trận TF-IDF
  tfidf_matrix = tfidf_vectorizer.fit_transform(data['combined_text'])
  return tfidf_matrix

def find_similar_books(title, tfidf_matrix, data, top_n):
  # Kiểm tra xem tên sách có trong danh sách không
  if title not in data['Title'].values:
    print("Book not found.")
    return []

  # Lấy chỉ mục của sách cần tìm tương đồng
  book_index = data.index[data['Title'] == title][0]

  # Tính độ tương đồng cosine giữa sách đã chọn và tất cả sách
  cosine_similarities = cosine_similarity(tfidf_matrix[book_index], tfidf_matrix).flatten()

  # Sắp xếp và lấy top_n cuốn sách tương đồng nhất (ngoại trừ chính sách đó)
  similar_indices = cosine_similarities.argsort()[-top_n-1:-1][::-1]
  similar_books = data.iloc[similar_indices]

  # hiển thị danh sách sách tương tự
  print(f"\nBooks similar to '{title}':")
  for i, row in similar_books.iterrows():
    print(f"- {row['Title']} (Author: {row['Author']})")

  return similar_books

# main
if __name__ == "__main__":
  data = load_data("data.csv")

  # Xử lý dữ liệu và tạo ma trận TF-IDF
  tfidf_df = preprocess_data(data)

  # Sách cần tìm tương tự
  book_title = "Cây Cam Ngọt Của Tôi"

  # Tìm sách tương tự
  similar_books = find_similar_books(book_title, tfidf_df, data, top_n=3)