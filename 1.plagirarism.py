import sys
import os
from nltk.tokenize import RegexpTokenizer

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QFileDialog, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Ensure nltk resources are downloaded
# Ensure nltk resources are downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

nltk.download('punkt')
nltk.download('stopwords')


# Text preprocessing
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text)
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)

# Jaccard Similarity
def jaccard_similarity(doc1, doc2):
    set1, set2 = set(doc1.split()), set(doc2.split())
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0

# GUI Application
class PlagiarismDetector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plagiarism Detection System")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Upload two text files to compare:")
        layout.addWidget(self.label)

        self.upload_btn1 = QPushButton("Upload File 1")
        self.upload_btn1.clicked.connect(self.upload_file1)
        layout.addWidget(self.upload_btn1)

        self.upload_btn2 = QPushButton("Upload File 2")
        self.upload_btn2.clicked.connect(self.upload_file2)
        layout.addWidget(self.upload_btn2)

        self.compare_btn = QPushButton("Compare Files")
        self.compare_btn.clicked.connect(self.compare_files)
        self.compare_btn.setEnabled(False)
        layout.addWidget(self.compare_btn)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.file1_path = None
        self.file2_path = None

    def upload_file1(self):
        self.file1_path, _ = QFileDialog.getOpenFileName(self, "Open File 1", "", "Text Files (*.txt)")
        if self.file1_path:
            self.label.setText(f"File 1: {os.path.basename(self.file1_path)} selected.")
            if self.file2_path:
                self.compare_btn.setEnabled(True)

    def upload_file2(self):
        self.file2_path, _ = QFileDialog.getOpenFileName(self, "Open File 2", "", "Text Files (*.txt)")
        if self.file2_path:
            self.label.setText(f"File 2: {os.path.basename(self.file2_path)} selected.")
            if self.file1_path:
                self.compare_btn.setEnabled(True)

    def compare_files(self):
        if not self.file1_path or not self.file2_path:
            self.result_text.setText("Please select both files.")
            return

        with open(self.file1_path, 'r') as file:
            text1 = preprocess_text(file.read())
        with open(self.file2_path, 'r') as file:
            text2 = preprocess_text(file.read())

        # Cosine Similarity
        vectorizer = CountVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity(vectors)[0, 1]

        # Jaccard Similarity
        jaccard_sim = jaccard_similarity(text1, text2)

        self.result_text.setText(f"Cosine Similarity: {cosine_sim:.4f}\nJaccard Similarity: {jaccard_sim:.4f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlagiarismDetector()
    window.show()
    sys.exit(app.exec_())
