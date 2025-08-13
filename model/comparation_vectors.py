# comparacao_vectorizers.py
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Configuração inicial
nltk.download('stopwords')
df = pd.read_csv('./model/data/phishing_dataset.csv')
df['text'] = df['text'].str.replace('\n', ' ')

# Pré-processamento (igual ao seu original)
stemmer = PorterStemmer()
stopwords_set = set(stopwords.words('english'))
corpus = df['text'].apply(lambda x: ' '.join(
    [stemmer.stem(word) for word in 
     x.lower().translate(str.maketrans('', '', string.punctuation)).split() 
     if word not in stopwords_set]
))

# Comparação direta
vectorizers = {
    "CountVectorizer": CountVectorizer(),
    "TF-IDF": TfidfVectorizer()
}

for name, vectorizer in vectorizers.items():
    X = vectorizer.fit_transform(corpus).toarray()
    X_train, X_test, y_train, y_test = train_test_split(X, df.label_num, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_jobs=-1).fit(X_train, y_train)
    print(f"\n🔹 {name}: Acurácia = {clf.score(X_test, y_test):.2%}")
    print("----------------------------------")