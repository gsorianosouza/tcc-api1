import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

data = [
    "isso é ótimo",
    "gostei muito",
    "muito bom",
    "péssimo serviço",
    "odiei isso",
    "muito ruim"
]

# 1 = feedback positivo e 0 = feedback negativo
labels = [1, 1, 1, 0, 0, 0]

# Pipeline: TF-IDF + Classificador
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', LogisticRegression())
])

pipeline.fit(data, labels)

# Salva o pipeline treinado em um arquivo .pkl
joblib.dump(pipeline, 'model/model.pkl')

print("Modelo treinado com sucesso e salvo em model/model.pkl")