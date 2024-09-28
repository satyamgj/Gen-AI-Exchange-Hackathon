from fastapi import APIRouter
from app.models.chatRequest import chatRequest
from app.models.chatReplyRequest import chatReplyRequest
# from app.core.chatbot import interactive_assistant
from app.service.answer_genration import getResponse,getChatResponse,getOtherRelatedQuestions

router = APIRouter()

@router.post("/query")
def query(request:chatRequest):
    # Calling a random number generator service (e.g., an external API)
    try:
       return getResponse(request.query)
    except Exception as e:
        return {"error": str(e)}

@router.post("/chat")
def chat(request:chatReplyRequest):
    # Calling a random number generator service (e.g., an external API)
    try:
       return getChatResponse(request.query,request.past_replies)
    except Exception as e:
        return {"error": str(e)}

@router.post("/relatedQuestions")
def relatedQuestion(request:chatRequest):
    try:
       return getOtherRelatedQuestions(request.query)
    except Exception as e:
        return {"error": str(e)}


