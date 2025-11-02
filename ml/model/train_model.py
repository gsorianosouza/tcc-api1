import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, label_binarize
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from core.database import SessionLocal
from ml.models.metrics import Metrics
from ml.utils.ml_utils import extract_features
from ml.model.model_manager_loader import dataset_path, model_path, encoder_path

df = pd.read_csv(dataset_path)

label_encoder = LabelEncoder()
df['label_encoded'] = label_encoder.fit_transform(df['type'])

print('Extraindo features')
X = pd.concat(df['url'].apply(extract_features).to_list(), ignore_index=True)
y = df['label_encoded']

print("Treinando o modelo RandomForest")
model = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42)
model.fit(X, y)

y_true = label_encoder.transform(df['type'])
y_pred = model.predict(X)

y_true_bin = label_binarize(y_true, classes=range(len(model.classes_)))
y_proba = model.predict_proba(X)

accuracy = accuracy_score(y_true, y_pred),
precision = precision_score(y_true, y_pred, average="weighted"),
recall = recall_score(y_true, y_pred, average="weighted"),
f1 = f1_score(y_true, y_pred, average="weighted"),
roc_auc = roc_auc_score(y_true_bin, y_proba, average="weighted", multi_class="ovr")

confusion_matrix_score = confusion_matrix(y_true, y_pred).tolist()

print("Salvando métricas no banco")

session = SessionLocal()
metrics = Metrics(
    accuracy=accuracy,
    precision=precision,
    recall=recall,
    f1_score=f1,
    roc_auc=roc_auc,
    confusion_matrix=confusion_matrix_score
)
session.add(metrics)
session.commit()
session.close()

joblib.dump(model, model_path)
joblib.dump(label_encoder, encoder_path)

print("Modelo e encoder salvos com sucesso!")