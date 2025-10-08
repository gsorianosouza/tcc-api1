import joblib
import os
import time
import threading
import json

class ModelManager:
    def __init__(self, model_path: str, encoder_path: str, metrics_path: str, check_interval: int = 10):
        self.model_path = model_path
        self.encoder_path = encoder_path
        self.metrics_path = metrics_path
        self.check_interval = check_interval

        self.model = None
        self.encoder = None
        self.metrics = None

        self._model_mtime = None
        self._encoder_mtime = None
        self._metrics_mtime = None

        self.load_model_and_metrics()
        self._start_monitor_thread()

    def load_model_and_metrics(self):
        self.model = joblib.load(self.model_path)
        self.encoder = joblib.load(self.encoder_path)
        self._model_mtime = os.path.getmtime(self.model_path)
        self._encoder_mtime = os.path.getmtime(self.encoder_path)
        print(f"Modelo e encoder carregados. Última modificação: {time.ctime(self._model_mtime)}")

        if os.path.exists(self.metrics_path):
            with open(self.metrics_path, "r") as f:
                self.metrics = json.load(f)
            self._metrics_mtime = os.path.getmtime(self.metrics_path)
            print(f"Métricas carregadas. Última modificação: {time.ctime(self._metrics_mtime)}")
        else:
            self.metrics = {}
            self._metrics_mtime = None
            print("Arquivo de métricas não encontrado.")

    def _start_monitor_thread(self):
        def monitor():
            while True:
                try:
                    model_mtime = os.path.getmtime(self.model_path)
                    encoder_mtime = os.path.getmtime(self.encoder_path)
                    metrics_mtime = os.path.getmtime(self.metrics_path) if os.path.exists(self.metrics_path) else None

                    if model_mtime != self._model_mtime or encoder_mtime != self._encoder_mtime:
                        print("Alteração detectada nos arquivos do modelo. Recarregando...")
                        self.load_model_and_metrics()
                    elif metrics_mtime != self._metrics_mtime:
                        print("Alteração detectada nas métricas. Recarregando...")
                        with open(self.metrics_path, "r") as f:
                            self.metrics = json.load(f)
                        self._metrics_mtime = metrics_mtime
                        print("Métricas recarregadas com sucesso.")
                except Exception as e:
                    print(f"Erro ao monitorar arquivos: {e}")
                time.sleep(self.check_interval)

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()