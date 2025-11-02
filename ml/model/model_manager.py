import joblib
import os
import time
import threading

class ModelManager:
    _instance = None
    _monitor_thread_started = False 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model_path: str, encoder_path: str, check_interval: int = 10):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        self.model_path = model_path
        self.encoder_path = encoder_path
        self.check_interval = check_interval

        self.model = None
        self.encoder = None

        self._model_mtime = None
        self._encoder_mtime = None

        self.try_load_model()

        if not ModelManager._monitor_thread_started:
            self.start_monitor_thread()
            ModelManager._monitor_thread_started = True

    def try_load_model(self):
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.encoder_path):
                self.model = joblib.load(self.model_path)
                self.encoder = joblib.load(self.encoder_path)
                self._model_mtime = os.path.getmtime(self.model_path)
                self._encoder_mtime = os.path.getmtime(self.encoder_path)
                print(f"✅  Modelo e encoder carregados. Última modificação: {time.ctime(self._model_mtime)}")
            else:
                print("⚠️  Modelo ou encoder ainda não existem. Aguardando treinamento.")

        except Exception as e:
            print(f"❌  Erro ao carregar modelo ou métricas: {e}")
            

    def start_monitor_thread(self):
        def monitor():
            while True:
                try:
                    model_mtime = os.path.getmtime(self.model_path) if os.path.exists(self.model_path) else None
                    encoder_mtime = os.path.getmtime(self.encoder_path) if os.path.exists(self.encoder_path) else None

                    if model_mtime and encoder_mtime:
                        if model_mtime != self._model_mtime or encoder_mtime != self._encoder_mtime:
                            print("🔁 Alteração detectada nos arquivos do modelo. Recarregando..")
                            self._try_load_model_and_metrics()

                except Exception as e:
                    print(f"⚠️  Erro ao monitorar arquivos: {e}")

                time.sleep(self.check_interval)

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()