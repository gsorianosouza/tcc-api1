from fastapi import WebSocket
from services.model_service import model_service
import asyncio 

class ModelController:
    
    connected_clients: list[WebSocket] = []

    @staticmethod
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        ModelController.connected_clients.append(websocket)
        print("Cliente conectado via WebSocket")

        try:
            while True:
                await websocket.receive_text()
        except Exception:
            print("Cliente desconectado")
        finally:
            ModelController.connected_clients.remove(websocket)
            
    @staticmethod
    async def _run_and_notify():
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, model_service.train_model)

        for ws in ModelController.connected_clients:
            try:
                await ws.send_json({
                    "message": "✅ Modelo treinado com sucesso!",
                    "model_path": result.get("model_path"),
                    "encoder_path": result.get("encoder_path")
                })
            except Exception:
                pass
    
    @staticmethod
    async def train_model():                
        asyncio.create_task(ModelController._run_and_notify())
        return {"message": "Treinamento iniciado. Você será notificado ao término."}
    
model_controller = ModelController()