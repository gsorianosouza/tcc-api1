import pandas as pd
import string, re, joblib
from fastapi import HTTPException
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from core.config import settings

suspicious_keywords = ['login','signin','verify','update','banking','account','secure','ebay','paypal']

def extract_features(url: str):
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
class ModelService:
    
    @staticmethod
    def train_model():
        try:
            df = pd.read_csv(settings.DATASET_PATH)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Dataset não encontrado")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao carregar dataset: {str(e)}")

        if 'url' not in df.columns or 'type' not in df.columns:
            raise HTTPException(status_code=400, detail="Dataset inválido: precisa conter colunas 'url' e 'type'")

        try:
            label_encoder = LabelEncoder()
            df['label_encoded'] = label_encoder.fit_transform(df['type'])

            X = df['url'].apply(extract_features)
            y = df['label_encoded']

            model = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42)
            model.fit(X, y)

            joblib.dump(model, settings.MODEL_PATH)
            joblib.dump(label_encoder, settings.ENCODER_PATH)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao treinar e salvar o modelo: {str(e)}")

        return {
            "message": "Modelo e encoder salvos com sucesso!",
            "model_path": settings.MODEL_PATH,
            "encoder_path": settings.ENCODER_PATH
        }

model_service = ModelService()