from pydantic import BaseModel
from enum import Enum
import os

models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../models")

class ModelName():
    GEMINI_2_0_FLASH_LITE = "gemini-2.0-flash-lite"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"

class ModelPath():
    Qwen_2_5_7B_Instruct = os.path.join(models_dir, "Qwen2.5-7B-Instruct")

class GeminiModelConfig(BaseModel):
    model: str
    temperature: float
    top_p: float
    max_tokens: int

class LocalModelConfig(BaseModel):
    model_path: ModelPath
    temperature: float
    top_p: float
    max_tokens: int