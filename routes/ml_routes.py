from fastapi import APIRouter
from schemas.feedback_schema import *

router = APIRouter()

@router.post("/feedback", 
             response_model=FeedbackResponse, 
             summary="Enviar feedback sobre uma previsão", 
             description="Permite que o usuário envie um feedback sobre a previsão do modelo."
)
def feedback(feedback: FeedbackRequest):
   print(f"Feedback recebido para {feedback.prediction_id}: {feedback.correct_label}")
   return FeedbackResponse(message="Feedback recebido com sucesso!")