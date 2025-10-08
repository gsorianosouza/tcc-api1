echo "Iniciando o banco de dados..."
python -m db.init_db

if [ ! -f "model/rf_model.pkl" ]; then
    echo "Treinando modelo de ML..."
    python -m model.train_model
fi

echo "Iniciando API..."
uvicorn main:app --host 0.0.0.0 --port 8000
