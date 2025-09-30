import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import string

from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from sklearn import svm
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from wordcloud import WordCloud

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv('./model/dataset/malicious_phish.csv')

# Distribuição de classes
plt.figure(figsize=(6,4))
sns.countplot(x='type', data=df)
plt.title('Distribution of URL Types')
plt.xlabel('Type')
plt.ylabel('Count')
plt.show()

# -----------------------------
# Wordclouds por tipo
# -----------------------------
types = ['phishing','malware','defacement','benign']
for t in types:
    urls = " ".join(i for i in df[df.type==t].url)
    wordcloud = WordCloud(width=1600, height=800, colormap='Paired').generate(urls)
    plt.figure(figsize=(12,14), facecolor='k')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.title(f"WordCloud - {t}", color='white')
    plt.show()

# -----------------------------
# Preprocessing
# -----------------------------
print(df.isnull().sum())
label_encoder = LabelEncoder()
df['label_encoded'] = label_encoder.fit_transform(df['type'])

suspicious_keywords = ['login','signin','verify','update','banking','account','secure','ebay','paypal']

def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['num_digits'] = sum(c.isdigit() for c in url)
    features['num_special_chars'] = sum(c in string.punctuation for c in url)
    features['num_subdomains'] = url.count('.') - 1
    features['has_ip'] = int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)))
    features['has_https'] = int('https' in url.lower())
    features['num_params'] = url.count('?')
    features['num_fragments'] = url.count('#')
    features['num_slashes'] = url.count('/')
    features['has_suspicious_words'] = int(any(word in url.lower() for word in suspicious_keywords))
    tld = url.split('.')[-1]
    features['tld_length'] = len(tld)
    features['is_common_tld'] = int(tld in ['com','org','net','edu','gov'])
    features['has_hex'] = int(bool(re.search(r'%[0-9a-fA-F]{2}', url)))
    features['repeated_chars'] = int(bool(re.search(r'(.)\1{3,}', url)))
    return pd.Series(features)

features_df = df['url'].apply(extract_features)
df = pd.concat([df, features_df], axis=1)

# Correlation heatmap
numeric_df = df.select_dtypes(include='number')
plt.figure(figsize=(10,6))
sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
plt.title('Feature Correlation Heatmap')
plt.show()

# -----------------------------
# Features and target
# -----------------------------
X = df.drop(columns=['url','type','label_encoded'])
y = df['label_encoded']

# -----------------------------
# Modelos
# -----------------------------
models = {
    'XGBoost': XGBClassifier(use_label_encoder=False, eval_metric='mlogloss'),
    'Random Forest': RandomForestClassifier(),
    'SVM': svm.LinearSVC(),
    'KNN': KNeighborsClassifier()
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
results_df = pd.DataFrame(columns=['Model','Fold','Accuracy','Precision','Recall','F1'])
train_accuracies = []

# -----------------------------
# Treinamento e avaliação
# -----------------------------
for name, model in models.items():
    print(f"\n===== {name} =====")
    
    # Cross-validation folds
    for fold, (train_idx, test_idx) in enumerate(cv.split(X, y),1):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, target_names=label_encoder.classes_, output_dict=True)
        
        results_df = pd.concat([
            results_df,
            pd.DataFrame({
                'Model':[name],
                'Fold':[fold],
                'Accuracy':[acc],
                'Precision':[report['macro avg']['precision']],
                'Recall':[report['macro avg']['recall']],
                'F1':[report['macro avg']['f1-score']]
            })
        ], ignore_index=True)
        
        print(f"\n--- Fold {fold} ---")
        print(f"Acurácia: {acc:.4f}")
        print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
    
    # Treino completo (overfitting check)
    model.fit(X, y)
    y_pred_train = model.predict(X)
    train_acc = accuracy_score(y, y_pred_train)
    train_accuracies.append(train_acc)
    print(f"{name} - Accuracy treino completo: {train_acc:.4f}")

# -----------------------------
# Resultados agregados
# -----------------------------
print("\nResumo de todas as métricas por fold:")
print(results_df)

mean_accuracies = results_df.groupby('Model')['Accuracy'].mean()
std_accuracies = results_df.groupby('Model')['Accuracy'].std()

# Comparação K-Fold
plt.figure(figsize=(10,6))
plt.bar(mean_accuracies.index, mean_accuracies.values, yerr=std_accuracies.values, capsize=5, alpha=0.7, label='CV Accuracy')
plt.scatter(mean_accuracies.index, train_accuracies, color='red', label='Train Accuracy', zorder=5)
plt.ylabel('Accuracy')
plt.title('Comparação Acurácia Média K-Fold vs Treino Completo')
plt.ylim(0,1.05)
plt.legend()
plt.show()

# Distribuição por fold
plt.figure(figsize=(10,6))
sns.boxplot(x='Model', y='Accuracy', data=results_df)
plt.title('Distribuição da Acurácia por Fold')
plt.show()
