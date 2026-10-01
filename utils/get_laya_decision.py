from brain.laya_interface import LayaRouter


async def get_laya_decision(user_message):
    laya_router = LayaRouter()
    laya_request = {
        "user_message": user_message,
    }
    decision_result = {
        "decision": laya_router.get_decision(laya_request),
    }
    return decision_result
