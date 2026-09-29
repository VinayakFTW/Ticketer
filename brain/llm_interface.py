from openai import OpenAI

from brain.config import ENVIRONMENT_VARIABLES
from utils.server_response import server_response
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR


class LLMRouter:
    def __init__(self, session_id=None):
        self.llm = OpenAI(
            api_key=ENVIRONMENT_VARIABLES.get("OPENAI_API_KEY"),
            base_url=ENVIRONMENT_VARIABLES.get("OPENAI_BASE_URL"),
        )
        self.mode = ENVIRONMENT_VARIABLES.get("MODE")
        self.session_id = session_id

    async def generate_response(self, session_data, user_message):
        session_data["messages"].append({"role": "user", "content": user_message})

        try:
            response = self.responses.create(
                model="auto",
                instructions=session_data["messages"][0]["content"],
                input=session_data["messages"][1:],
            )

            assistant_message = response.output_text
            session_data["messages"].append(response.output)
            return server_response(
                status_code=SUCCESS,
                data={"assistant_message": assistant_message},
            )
        except Exception as e:
            return server_response(
                status_code=INTERNAL_SERVER_ERROR,
            )
