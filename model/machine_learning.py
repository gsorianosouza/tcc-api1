import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import tree
from sklearn.model_selection import KFold
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier

from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt
from sklearn.semi_supervised import LabelSpreading

legitimate_df = pd.read_csv("./model/dataset/legitimate_dataset.csv")
phishing_df = pd.read_csv("./model/dataset/phishing_dataset.csv")

df = pd.concat([legitimate_df, phishing_df], axis=0)
df = df.sample(frac=1, random_state=42)

df = df.drop('URL', axis=1)

df = df.drop_duplicates()

legit_df = df[df['label'] == 0]
phish_df = df[df['label'] == 1]

legit_sampled = legit_df.sample(n=len(phish_df), random_state=42)
df = pd.concat([legit_sampled, phish_df], axis=0)
df = df.sample(frac=1, random_state=42)

X = df.drop('label', axis=1)
Y = df['label']

svm_model = svm.LinearSVC() # Support Vector Machine (SVM)

rf_model = RandomForestClassifier() # Random Forest

ab_model = AdaBoostClassifier() # AdaBoost

nb_model = GaussianNB() # Gaussian Naive Bayes

semi_model = LabelSpreading(kernel="knn", n_neighbors=7)


# K-Fold (K5) => Fiz isso pra avaliar e evitar o overfiting

K = 5
kf = KFold(n_splits=K, shuffle=True, random_state=42)

def calculate_measures(TN, TP, FN, FP):
    model_accuracy = (TP + TN) / (TP + TN + FN + FP)
    model_precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    model_recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    return model_accuracy, model_precision, model_recall


rf_accuracy_list, rf_precision_list, rf_recall_list = [], [], []
ab_accuracy_list, ab_precision_list, ab_recall_list = [], [], []
svm_accuracy_list, svm_precision_list, svm_recall_list = [], [], []
nb_accuracy_list, nb_precision_list, nb_recall_list = [], [], []
semi_accuracy_list, semi_precision_list, semi_recall_list = [], [], []

for train_index, test_index in kf.split(X):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    Y_train, Y_test = Y.iloc[train_index], Y.iloc[test_index]
    
    # ----- RANDOM FOREST ----- #
    rf_model.fit(X_train, Y_train)
    rf_predictions = rf_model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_true=Y_test, y_pred=rf_predictions).ravel()
    rf_accuracy, rf_precision, rf_recall = calculate_measures(tn, tp, fn, fp)
    rf_accuracy_list.append(rf_accuracy)
    rf_precision_list.append(rf_precision)
    rf_recall_list.append(rf_recall)

    # ----- SUPPORT VECTOR MACHINE ----- #
    svm_model.fit(X_train, Y_train)
    svm_predictions = svm_model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_true=Y_test, y_pred=svm_predictions).ravel()
    svm_accuracy, svm_precision, svm_recall = calculate_measures(tn, tp, fn, fp)
    svm_accuracy_list.append(svm_accuracy)
    svm_precision_list.append(svm_precision)
    svm_recall_list.append(svm_recall)

    # ----- ADABOOST ----- #
    ab_model.fit(X_train, Y_train)
    ab_predictions = ab_model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_true=Y_test, y_pred=ab_predictions).ravel()
    ab_accuracy, ab_precision, ab_recall = calculate_measures(tn, tp, fn, fp)
    ab_accuracy_list.append(ab_accuracy)
    ab_precision_list.append(ab_precision)
    ab_recall_list.append(ab_recall)
    
     # ----- LABEL SPREADING (Semi-supervisionado) ----- #
    rng = np.random.RandomState(42)
    mask = rng.rand(len(Y_train)) < 0.7
    Y_train_semi = Y_train.copy()
    Y_train_semi[mask] = -1
    
    semi_model.fit(X_train, Y_train_semi)
    semi_predictions = semi_model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_true=Y_test, y_pred=semi_predictions).ravel()
    semi_accuracy, semi_precision, semi_recall = calculate_measures(tn, tp, fn, fp)
    semi_accuracy_list.append(semi_accuracy)
    semi_precision_list.append(semi_precision)
    semi_recall_list.append(semi_recall)


RF_accuracy = sum(rf_accuracy_list) / len(rf_accuracy_list)
RF_precision = sum(rf_precision_list) / len(rf_precision_list)
RF_recall = sum(rf_recall_list) / len(rf_recall_list)

print()

print("Random Forest accuracy ==> ", RF_accuracy)
print("Random Forest precision ==> ", RF_precision)
print("Random Forest recall ==> ", RF_recall)

print("============================================================")

AB_accuracy = sum(ab_accuracy_list) / len(ab_accuracy_list)
AB_precision = sum(ab_precision_list) / len(ab_precision_list)
AB_recall = sum(ab_recall_list) / len(ab_recall_list)

print("AdaBoost accuracy ==> ", AB_accuracy)
print("AdaBoost precision ==> ", AB_precision)
print("AdaBoost recall ==> ", AB_recall)

print("============================================================")


SVM_accuracy = sum(svm_accuracy_list) / len(svm_accuracy_list)
SVM_precision = sum(svm_precision_list) / len(svm_precision_list)
SVM_recall = sum(svm_recall_list) / len(svm_recall_list)

print("Support Vector Machine accuracy ==> ", SVM_accuracy)
print("Support Vector Machine precision ==> ", SVM_precision)
print("Support Vector Machine recall ==> ", SVM_recall)


print("============================================================")

SEMI_accuracy = sum(semi_accuracy_list) / len(semi_accuracy_list)
SEMI_precision = sum(semi_precision_list) / len(semi_precision_list)
SEMI_recall = sum(semi_recall_list) / len(semi_recall_list)

print("Semi accuracy ==> ", SEMI_accuracy)
print("Semi precision ==> ", SEMI_precision)
print("Semi recall ==> ", SEMI_recall)

print("============================================================")
        
data = {
        'accuracy': [SVM_accuracy, RF_accuracy, AB_accuracy, SEMI_accuracy],
        'precision': [SVM_precision, RF_precision, AB_precision, SEMI_precision],
        'recall': [SVM_recall, RF_recall, AB_recall, SEMI_recall]
        }

index = ['SVM', 'RF', 'AB', 'SEMI']

df_results = pd.DataFrame(data=data, index=index)

ax = df_results.plot.bar(rot=0)
plt.show()