import string
import joblib
import numpy as np
import pandas as pd
import os

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

nltk.download('stopwords')

if not os.path.exists('model'):
    os.makedirs('model')

try:
    df = pd.read_csv('./model/data/phishing_dataset.csv')
    df['URL'] = df['URL'].apply(lambda x: x.replace('\n', ' '))
except FileNotFoundError:
    print("ERRO: Arquivo './model/data/phishing_dataset.csv' não encontrado!")
    exit(1)

df['label_num'] = df['Label'].map({'good': 0, 'bad': 1})

stemmer = PorterStemmer()
corpus = []
stopwords_set = set(stopwords.words('english'))

for i in range(len(df)):
    text = df['URL'].iloc[i].lower()
    text = text.translate(str.maketrans('', '', string.punctuation)).split()
    text = [stemmer.stem(word) for word in text if word not in stopwords_set]
    text = ' '.join(text)
    corpus.append(text)


vectorizer = TfidfVectorizer(max_features=5000)
X =  vectorizer.fit_transform(corpus)
y = df['label_num']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Added random_state

clf = RandomForestClassifier(n_jobs=-1)
clf.fit(X_train, y_train)


accuracy = clf.score(X_test, y_test)
print(f"\n✅ Acurácia do modelo: {accuracy:.2%}")
print("\n📊 Métricas detalhadas:")
print(classification_report(y_test, clf.predict(X_test)))


sample_email = df['URL'].values[10]
processed_email = ' '.join(
    [stemmer.stem(word) for word in 
     sample_email.lower().translate(str.maketrans('', '', string.punctuation)).split()
     if word not in stopwords_set]
)

prediction = clf.predict(vectorizer.transform([processed_email]).toarray())
print(f"\n🔍 Email de exemplo classificado como: {'SPAM' if prediction[0] == 1 else 'HAM'}")


joblib.dump((clf, vectorizer), 'model/model.pkl')
print("\n💾 Modelo salvo em 'model/model.pkl'")