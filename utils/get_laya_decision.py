from brain.laya_interface import LAYA


async def get_laya_decision(user_message):
    laya_request = {
        "user_message": user_message,
    }
    decision_result = {
        "decision": LAYA.get_decision(laya_request),
    }
    return decision_result
