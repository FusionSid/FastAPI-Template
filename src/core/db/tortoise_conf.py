import os
from dotenv import load_dotenv

load_dotenv()

TORTOISE_CONFIG = {
    "connections": {"default": os.environ["DATABASE_URL"]},
    "apps": {
        "models": {
            "models": ["core.models.example_model"],
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "UTC",
}
