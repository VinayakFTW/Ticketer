from brain.laya_interface import LAYA


async def get_laya_decision(user_message):
    laya_request = {
        "user_message": user_message,
    }
    decision = await LAYA.get_decision(laya_request)
    decision_result = {
        "decision": decision.model_dump(),
    }
    return decision_result
