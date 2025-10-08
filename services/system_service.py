class SystemService:
    
    @staticmethod
    def get_status():
        return {
            "status": "ok",
        }
        

system_service = SystemService()