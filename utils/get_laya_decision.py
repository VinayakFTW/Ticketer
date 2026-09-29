from brain.laya_interface import LayaRouter


async def get_laya_decision(session_id, user_message):
    laya_router = LayaRouter()
    laya_request = {
        "user_message": user_message,
    }
    decision_result = {
        "decision": laya_router.get_decision(laya_request),
        "session_id": session_id,
    }
    return decision_result
