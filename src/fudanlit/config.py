"""从项目根目录的 .env 读取配置。"""
from __future__ import annotations

import os

from dotenv import load_dotenv


def load_config() -> dict:
    load_dotenv()
    return {
        "mailto": os.getenv("MAILTO", ""),
        "semantic_scholar_api_key": os.getenv("SEMANTIC_SCHOLAR_API_KEY", ""),
    }
