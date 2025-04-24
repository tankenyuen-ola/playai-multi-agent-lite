from core.config.model_config import GeminiModelConfig, LocalModelConfig, ModelName, ModelPath

predefine_gemini_configs = {
        "router_agent": GeminiModelConfig(
            model=ModelName.GEMINI_2_0_FLASH,
            temperature=0.5,
            top_p=1,
            max_tokens=256
        ),
        "agent_1": GeminiModelConfig(
            model=ModelName.GEMINI_2_0_FLASH,
            temperature=1,
            top_p=0.5,
            max_tokens=512
        ),
        "agent_2": GeminiModelConfig(
            model=ModelName.GEMINI_2_0_FLASH,
            temperature=1,
            top_p=0.7,
            max_tokens=512
        ),
        "agent_3": GeminiModelConfig(
            model=ModelName.GEMINI_2_0_FLASH,
            temperature=1,
            top_p=0.6,
            max_tokens=512
        ),
        "agent_4": GeminiModelConfig(
            model=ModelName.GEMINI_2_0_FLASH,
            temperature=1,
            top_p=0.5,
            max_tokens=512
        )
    }

predefine_qwen_configs = {
    "router_agent": LocalModelConfig(
        model=ModelPath.Qwen_2_5_7B_Instruct,
        temperature=0.5,
        top_p=1,
        max_tokens=1024
    ),
    "agent_1": LocalModelConfig(
        model=ModelPath.Qwen_2_5_7B_Instruct,
        temperature=0.8,
        top_p=1,
        max_tokens=1024
    ),
    "agent_2": LocalModelConfig(
        model=ModelPath.Qwen_2_5_7B_Instruct,
        temperature=1,
        top_p=0.7,
        max_tokens=1024
    ),
    "agent_3": LocalModelConfig(
        model=ModelPath.Qwen_2_5_7B_Instruct,
        temperature=1,
        top_p=0.6,
        max_tokens=1024
    ),
    "agent_4": LocalModelConfig(
        model=ModelPath.Qwen_2_5_7B_Instruct,
        temperature=0.8,
        top_p=0.9,
        max_tokens=1024
    )
}

# "/data/llamafactory_model/Qwen2.5-7B-Instruct"