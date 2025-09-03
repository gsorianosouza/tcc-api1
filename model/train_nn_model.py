import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
import matplotlib.pyplot as plt
from core.config import settings
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
from sklearn.utils.class_weight import compute_class_weight

from tensorflow import keras
from keras import layers
import seaborn as sns
import os

os.makedirs("./model/results", exist_ok=True)

SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)

df = pd.read_csv(settings.DATA_PATH)

print(f"Shape do dataset: {df.shape}")
print(f"\nDistribuição das classes:")
print(df["CLASS_LABEL"].value_counts())
print(f"\nProporção das classes:")
print(df["CLASS_LABEL"].value_counts(normalize=True))

X = df.drop(columns=["id", "CLASS_LABEL"])
y = df["CLASS_LABEL"].astype(int)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

input_dim = X_scaled.shape[1]
print(f"\nDimensão dos dados: {input_dim} features")

def make_model(input_dim: int, learning_rate: float = 1e-4) -> keras.Model:
    inputs = keras.Input(shape=(input_dim,))
    x = layers.Dense(64, activation="relu", kernel_regularizer=keras.regularizers.l2(1e-3))(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)
    x = layers.Dense(32, activation="relu", kernel_regularizer=keras.regularizers.l2(1e-3))(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(16, activation="relu")(x)
    outputs = layers.Dense(1, activation="sigmoid")(x)

    model = keras.Model(inputs, outputs)
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=["accuracy", 
                keras.metrics.Precision(name='precision'),
                keras.metrics.Recall(name='recall'), 
                keras.metrics.AUC(name='auc')]
    )
    return model

kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

results = { 
    "Accuracy": [], "Precision": [], "Recall": [], "F1": [], "Auc": []
}

fold_details = []

for fold, (train_idx, test_idx) in enumerate(kfold.split(X_scaled, y), 1):
    
    print(f"\n{'='*20} Fold {fold} {'='*20}")
    
    X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    print(f"Distribuição Treino: {np.bincount(y_train)}")
    print(f"Distribuição Teste:  {np.bincount(y_test)}")
    
    X_train_split, X_val, y_train_split, y_val = train_test_split(
        X_train, y_train, test_size=0.2, stratify=y_train, random_state=SEED
    )
    
    class_weights = compute_class_weight(
        class_weight="balanced",
        classes=np.unique(y_train),
        y=y_train
    )
    class_weights = dict(enumerate(class_weights))
    print(f"Class weights: {class_weights}")

    model = make_model(input_dim)

    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_auc", patience=10, restore_best_weights=True, 
            verbose=1, mode="max"
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_auc", factor=0.5, patience=5, min_lr=1e-7, 
            verbose=1, mode="max"
        )
    ]

    history = model.fit(
        X_train_split, y_train_split,
        epochs=100,
        batch_size=256,
        validation_data=(X_val, y_val),
        callbacks=callbacks,
        class_weight=class_weights,
        verbose=1
    )
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    available_metrics = list(history.history.keys())
    print(f"\nMétricas disponíveis: {available_metrics}")
    
    metrics_to_plot = ['loss', 'accuracy', 'precision', 'recall', 'auc']
    
    for i, metric in enumerate(metrics_to_plot):
        row, col = i // 3, i % 3
        
        train_metric = f"{metric}" if metric in history.history else None
        val_metric = f"val_{metric}" if f"val_{metric}" in history.history else None
        
        if train_metric and val_metric:
            axes[row, col].plot(history.history[train_metric], label=f'Treino {metric}')
            axes[row, col].plot(history.history[val_metric], label=f'Val {metric}')
            axes[row, col].set_title(f'Fold {fold} - {metric.capitalize()}')
            axes[row, col].set_xlabel('Épocas')
            axes[row, col].set_ylabel(metric.capitalize())
            axes[row, col].legend()
            axes[row, col].grid(True)
        else:
            axes[row, col].set_title(f'Metric {metric} not available')
            axes[row, col].text(0.5, 0.5, f'{metric} not found', 
                               ha='center', va='center', transform=axes[row, col].transAxes)
    
    if len(metrics_to_plot) < 6:
        for i in range(len(metrics_to_plot), 6):
            row, col = i // 3, i % 3
            fig.delaxes(axes[row, col])
    
    plt.tight_layout()
    plt.savefig(f"./model/results/training_fold_{fold}_detailed.png")
    plt.close()

    y_prob = model.predict(X_test, verbose=0).ravel()
    y_pred = (y_prob >= 0.5).astype(int)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)

    results["Accuracy"].append(acc)
    results["Precision"].append(prec)
    results["Recall"].append(rec)
    results["F1"].append(f1)
    results["Auc"].append(auc)

    fold_details.append({
        'fold': fold,
        'train_distribution': np.bincount(y_train),
        'test_distribution': np.bincount(y_test),
        'metrics': {
            'accuracy': acc, 'precision': prec, 'recall': rec, 
            'f1': f1, 'auc': auc
        },
        'confusion_matrix': confusion_matrix(y_test, y_pred)
    })

    print(f"\nResultados Fold {fold}:")
    print(f"Acurácia: {acc:.4f} | Precisão: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Legítimo', 'Phishing'],
                yticklabels=['Legítimo', 'Phishing'])
    plt.title(f'Fold {fold} - Matriz de Confusão')
    plt.ylabel('Verdadeiro')
    plt.xlabel('Predito')
    plt.savefig(f"./model/results/confusion_matrix_fold_{fold}.png")
    plt.close()

print(f"\n{'='*40}")
print("ANÁLISE DETALHADA DOS RESULTADOS")
print(f"{'='*40}")

print("\n===== MÉDIAS DOS FOLDS =====")
for metric, values in results.items():
    if values:
        print(f"{metric}: {np.mean(values):.4f} ± {np.std(values):.4f}")

print(f"\n{'='*40}")
print("ANÁLISE POR FOLD:")
print(f"{'='*40}")

for detail in fold_details:
    print(f"\nFold {detail['fold']}:")
    print(f"  Distribuição Treino: {detail['train_distribution']}")
    print(f"  Distribuição Teste:  {detail['test_distribution']}")
    print(f"  Acurácia:  {detail['metrics']['accuracy']:.4f}")
    print(f"  Precisão:  {detail['metrics']['precision']:.4f}")
    print(f"  Recall:    {detail['metrics']['recall']:.4f}")
    print(f"  F1:        {detail['metrics']['f1']:.4f}")
    print(f"  AUC:       {detail['metrics']['auc']:.4f}")

auc_scores = [detail['metrics']['auc'] for detail in fold_details]
worst_fold_idx = np.argmin(auc_scores)
worst_fold = fold_details[worst_fold_idx]

print(f"\n{'='*40}")
print(f"FOLD COM PIOR DESEMPENHO (Fold {worst_fold['fold']}):")
print(f"{'='*40}")
print(f"AUC: {worst_fold['metrics']['auc']:.4f}")
print(f"Distribuição Treino: {worst_fold['train_distribution']}")
print(f"Distribuição Teste:  {worst_fold['test_distribution']}")

results_df = pd.DataFrame({
    'Fold': [f'Fold {i+1}' for i in range(5)],
    'Accuracy': results["Accuracy"],
    'Precision': results["Precision"],
    'Recall': results["Recall"],
    'F1': results["F1"],
    'AUC': results["Auc"]
})

results_df.to_csv("./model/results/detailed_results.csv", index=False)
print(f"\nResultados detalhados salvos em: ./model/results/detailed_results.csv")

print("\nTreinando modelo final em todos os dados...")

final_model = make_model(input_dim)

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(y),
    y=y
)
class_weights = dict(enumerate(class_weights))

callbacks = [
    keras.callbacks.EarlyStopping(
        monitor="val_auc", patience=10, restore_best_weights=True, 
        verbose=1, mode="max"
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor="val_auc", factor=0.5, patience=5, min_lr=1e-7, 
        verbose=1, mode="max"
    )
]

X_train, X_val, y_train, y_val = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=SEED
)

history = final_model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=256,
    validation_data=(X_val, y_val),
    callbacks=callbacks,
    class_weight=class_weights,
    verbose=1
)

final_model.save("./model/final_model.h5")

joblib.dump(scaler, "./model/scaler.pkl")

print("\nModelo final salvo em ./model/final_model.h5")
print("Scaler salvo em ./model/scaler.pkl")

y_prob_final = final_model.predict(X_val, verbose=0).ravel()
y_pred_final = (y_prob_final >= 0.5).astype(int)

acc_final = accuracy_score(y_val, y_pred_final)
prec_final = precision_score(y_val, y_pred_final, zero_division=0)
rec_final = recall_score(y_val, y_pred_final)
f1_final = f1_score(y_val, y_pred_final)
auc_final = roc_auc_score(y_val, y_prob_final)

print("\n===== MÉTRICAS DO MODELO FINAL (conjunto de validação) =====")
print(f"Acurácia: {acc_final:.4f}")
print(f"Precisão: {prec_final:.4f}")
print(f"Recall:   {rec_final:.4f}")
print(f"F1:       {f1_final:.4f}")
print(f"AUC:      {auc_final:.4f}")

cm_final = confusion_matrix(y_val, y_pred_final)
plt.figure(figsize=(6, 5))
sns.heatmap(cm_final, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Legítimo', 'Phishing'],
            yticklabels=['Legítimo', 'Phishing'])
plt.title('Modelo Final - Matriz de Confusão')
plt.ylabel('Verdadeiro')
plt.xlabel('Predito')
plt.savefig("./model/results/final_model_confusion_matrix.png")
plt.close()