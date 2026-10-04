import json

from openai import AsyncOpenAI

from brain.config import ENVIRONMENT_VARIABLES, RESPONSE_FORMAT
from brain.config import SUMMARY_PROMPT, SYSTEM_PROMPT, TicketSummary
from constants.server_codes import SUCCESS, INTERNAL_SERVER_ERROR


class LLMRouter:
    def __init__(self):
        self.llm = AsyncOpenAI(
            api_key=ENVIRONMENT_VARIABLES.get("OPENAI_API_KEY"),
            base_url=ENVIRONMENT_VARIABLES.get("OPENAI_BASE_URL"),
        )
        self.mode = ENVIRONMENT_VARIABLES.get("MODE")

    async def generate_response(self, user_message):

        try:
            response = await self.llm.responses.create(
                model="auto",
                instructions=SYSTEM_PROMPT,
                input=[{"role": "user", "content": user_message}],
            )

            assistant_message = response.output_text
            return {"status_code": SUCCESS, "assistant_message": assistant_message}
        except Exception as e:
            return {"status_code": INTERNAL_SERVER_ERROR, "assistant_message": None}

    async def generate_summary(self, user_message, laya_decision):
        content = (
            f"User Message:\n{user_message}\n\n"
            f"Ticket Decision (Metadata):\n{json.dumps(laya_decision)}"
        )
        try:
            response = await self.llm.beta.chat.completions.parse(
                model="auto",
                messages=[
                    {"role": "system", "content": SUMMARY_PROMPT},
                    {"role": "user", "content": content},
                ],
            )

            raw_content = response.choices[0].message.content.strip()

            try:
                data = json.loads(raw_content)
                summary_text = (
                    data.get("summary", raw_content)
                    if isinstance(data, dict)
                    else raw_content
                )
            except json.JSONDecodeError:
                summary_text = raw_content

            return {"status_code": SUCCESS, "assistant_message": summary_text}
        except Exception as e:
            from utils.logger import debug_logger

            debug_logger()
            return {"status_code": INTERNAL_SERVER_ERROR, "assistant_message": None}
