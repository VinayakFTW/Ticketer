from openai import OpenAI
import os, uuid, json
from dotenv import load_dotenv

from brain.config import SYSTEM_PROMPT

load_dotenv()


class LLMInterface:
    def __init__(self, mode="local"):
        self.llm = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        )
        self.mode = mode

    async def create_chat_session(self):
        session_id = str(uuid.uuid4())
        if self.mode == "local":
            session_file = f"sessions/session_{session_id}.json"
            with open(session_file, "w") as f:
                json.dump(
                    {"messages": [{"role": "system", "content": SYSTEM_PROMPT}]}, f
                )
        elif self.mode == "mongo":
            pass  # will implement later, good night time
        else:
            raise ValueError("Invalid mode. Choose 'local' or 'mongo'.")

        return session_id

    async def generate_response(self, session_id, user_message):
        session_data = None
        if self.mode == "local":
            session_file = f"sessions/session_{session_id}.json"
            with open(session_file, "r") as f:
                session_data = json.load(f)
        elif self.mode == "mongo":
            pass  # will implement

        session_data["messages"].append({"role": "user", "content": user_message})

        response = self.responses.create(
            model="auto",
            instructions=session_data["messages"][0]["content"],
            input=session_data["messages"][1:],
        )

        assistant_message = response.output_text
        session_data["messages"].append(response.output)

        with open(session_file, "w") as f:
            json.dump(session_data, f)

        return assistant_message
