import os

SYSTEM_PROMPT = """
You are a helpful assistant that provides information about the Ticketer system.
You should only provide factual information about the system and avoid making up information.

"""

ENVIRONMENT_VARIABLES = {
    "OPENAI_BASE_URL": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
    "POSTGRES_URL": os.environ.get("POSTGRES_URL", ""),
}
