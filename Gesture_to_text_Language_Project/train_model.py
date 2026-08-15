import csv, json
from pathlib import Path
import joblib, numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from config import DATA_DIR, MODEL_DIR, MODEL_PATH, LABELS_PATH

def main():
    X, y = [], []
    for path in sorted(Path(DATA_DIR).glob("*.csv")):
        with open(path, newline="") as f:
            for row in list(csv.DictReader(f)):
                y.append(row["label"]); X.append([float(row[f"f{i}"]) for i in range(63)])
    if not X: raise RuntimeError("Collect data first.")
    if len(set(y)) < 2: raise RuntimeError("Need at least two sign classes.")
    X=np.asarray(X,dtype=np.float32); y=np.asarray(y)
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
    model=RandomForestClassifier(n_estimators=250,random_state=42,n_jobs=-1,class_weight="balanced")
    model.fit(Xtr,ytr); pred=model.predict(Xte)
    print("Accuracy:", accuracy_score(yte,pred))
    print(classification_report(yte,pred))
    print("Confusion matrix:\n",confusion_matrix(yte,pred))
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(model,MODEL_PATH)
    LABELS_PATH.write_text(json.dumps(sorted(set(y)),indent=2))
    print("Saved:", MODEL_PATH)

if __name__=="__main__": main()
