from core.prompt.agent_predefine_prompt import *
from core.llmapi.gemini_api import generate_text, generate_text_with_stream
from core.llmapi.local_llm_api import local_model_generate_text, local_model_generate_text_stream
from core.prompt.gemini_prompt import GeminiPrompt
import random
from core.config.logging_config import setup_logger
import logging

setup_logger()
logger = logging.getLogger(__name__)

class AgentOrchestra:
    def __init__(self):
        self.agent_router_system_prompt = agent_router_system_prompt
        self.agent_background_prompt = agent_template_prompt
        self.agent_humorist_character = humorist_character
        self.agent_empathetic_listener_character = empathetic_listener_character
        self.agent_contrarian_character = contrarian_character
        self.agent_whatever_character = whatever_character
        self.emotion_guide_list = emotion_guide_list
        self.humorist_character_speech_reference = humorist_character_speech_reference
        self.empathetic_listener_character_speech_reference = empathetic_listener_character_speech_reference
        self.contrarian_character_speech_reference = contrarian_character_speech_reference
        self.whatever_character_speech_reference = whatever_character_speech_reference


    def init_router_agent_prompt(self, chat_history, current_question):
        return self.agent_router_system_prompt.format(CHAT_HISTORY=chat_history, CURRENT_QUESTION=current_question)

  
    def init_agent_prompt(self, chat_history, current_question, emotion_guide):
        return {"agent_1": self.agent_background_prompt.format(CHARACTER_PROFILE=self.agent_humorist_character, CHAT_HISTORY=chat_history, CURRENT_QUESTION=current_question, EMOTION_GUIDE=emotion_guide, SPEECH_REFERENCE=self.humorist_character_speech_reference),
                "agent_2": self.agent_background_prompt.format(CHARACTER_PROFILE=self.agent_empathetic_listener_character, CHAT_HISTORY=chat_history, CURRENT_QUESTION=current_question, EMOTION_GUIDE=emotion_guide, SPEECH_REFERENCE=self.empathetic_listener_character_speech_reference),
                "agent_3": self.agent_background_prompt.format(CHARACTER_PROFILE=self.agent_contrarian_character, CHAT_HISTORY=chat_history, CURRENT_QUESTION=current_question, EMOTION_GUIDE=emotion_guide, SPEECH_REFERENCE=self.contrarian_character_speech_reference)   ,
                "agent_4": self.agent_background_prompt.format(CHARACTER_PROFILE=self.agent_whatever_character, CHAT_HISTORY=chat_history, CURRENT_QUESTION=current_question, EMOTION_GUIDE=emotion_guide, SPEECH_REFERENCE=self.whatever_character_speech_reference)}
    

    def init_agent_model_config(self, model_configs:dict):
        return {"router_agent": model_configs["router_agent"],
                "agent_1": model_configs["agent_1"],
                "agent_2": model_configs["agent_2"],
                "agent_3": model_configs["agent_3"],
                "agent_4": model_configs["agent_4"]}

    # def init_agent_model_config(self, model_configs: dict):
    #     return {
    #         "router_agent": LocalModelConfig(**model_configs["router_agent"]),
    #         "agent_1": LocalModelConfig(**model_configs["agent_1"]),
    #         "agent_2": LocalModelConfig(**model_configs["agent_2"]),
    #         "agent_3": LocalModelConfig(**model_configs["agent_3"]),
    #         "agent_4": LocalModelConfig(**model_configs["agent_4"]),
    #     }
    
    def get_router_agent_response(self, current_question, router_agent_prompt, _model_configs):
        if _model_configs.model.startswith("gemini"):
            prompt = GeminiPrompt(prompt=current_question, system_instruction=router_agent_prompt)
            return generate_text(prompt, _model_configs)
        else:
            return local_model_generate_text(
                prompt=current_question,
                system_instruction=router_agent_prompt,
                model_configs=_model_configs
        )

    def router_to_agent(self, current_question, router_agent_response, agent_prompt, model_configs):
        for agent_key in ["agent_1", "agent_2", "agent_3", "agent_4"]:
            if agent_key in router_agent_response:
                agent_model_config = model_configs[agent_key]
                print(agent_model_config)
                if agent_model_config.model.startswith("gemini"):
                    prompt = GeminiPrompt(prompt=current_question, system_instruction=agent_prompt[agent_key])
                    return generate_text(prompt, agent_model_config)
                else:
                    return local_model_generate_text(
                        prompt=current_question,
                        system_instruction=agent_prompt[agent_key],
                        model_configs=agent_model_config
                    )
        logger.info("没有找到合适的代理")
        return ""

    def multi_agent_response_with_stream_gemini(self, chat_history, current_question, model_configs:dict):
        router_agent_prompt = self.init_router_agent_prompt(chat_history, current_question)
        emotion_guide = random.choice(self.emotion_guide_list)
        logger.info("emotion guide index: {self.emotion_guide_list.index(emotion_guide)}")
        agent_prompt = self.init_agent_prompt(chat_history, current_question, emotion_guide)
        _model_configs = self.init_agent_model_config(model_configs)

        router_agent_response = self.get_router_agent_response(current_question, router_agent_prompt, _model_configs["router_agent"])
        logger.info("router_agent_response:{router_agent_response}" )

        if "agent_1" in router_agent_response:
            for chunk in generate_text_with_stream(GeminiPrompt(prompt=current_question, system_instruction=agent_prompt["agent_1"]), _model_configs["agent_1"]):
                yield chunk
        elif "agent_2" in router_agent_response:
            for chunk in generate_text_with_stream(GeminiPrompt(prompt=current_question, system_instruction=agent_prompt["agent_2"]), _model_configs["agent_2"]):
                yield chunk
        elif "agent_3" in router_agent_response:
            for chunk in generate_text_with_stream(GeminiPrompt(prompt=current_question, system_instruction=agent_prompt["agent_3"]), _model_configs["agent_3"]):
                yield chunk
        elif "agent_4" in router_agent_response:
            for chunk in generate_text_with_stream(GeminiPrompt(prompt=current_question, system_instruction=agent_prompt["agent_4"]), _model_configs["agent_4"]):
                yield chunk
        else:
            yield ""
            logger.info("没有找到合适的代理")


    def multi_agent_response_local(self, chat_history, current_question, model_configs:dict):
        router_agent_prompt = self.init_router_agent_prompt(chat_history, current_question)
        emotion_guide = random.choice(self.emotion_guide_list)
        logger.info("emotion guide index: {self.emotion_guide_list.index(emotion_guide)}")
        agent_prompt = self.init_agent_prompt(chat_history, current_question, emotion_guide)
        _model_configs = self.init_agent_model_config(model_configs)

        router_agent_response = self.get_router_agent_response(current_question, router_agent_prompt, _model_configs["router_agent"])
        logger.info("router_agent_response:{router_agent_response}" )

        for agent_key in ["agent_1", "agent_2", "agent_3", "agent_4"]:
            if agent_key in router_agent_response:
                agent_model_config = model_configs[agent_key]
                print(agent_model_config)
                if agent_model_config.model.startswith("gemini"):
                    prompt = GeminiPrompt(prompt=current_question, system_instruction=agent_prompt[agent_key])
                    return generate_text(prompt, agent_model_config)
                else:
                    return local_model_generate_text(
                        prompt=current_question,
                        system_instruction=agent_prompt[agent_key],
                        model_configs=agent_model_config
                    )
        logger.info("没有找到合适的代理")
        return ""
        
        return self.router_to_agent(current_question, router_agent_response, agent_prompt, _model_configs)
    
    def multi_agent_response_local_stream(self, chat_history, current_question, model_configs:dict):
        router_agent_prompt = self.init_router_agent_prompt(chat_history, current_question)
        emotion_guide = random.choice(self.emotion_guide_list)
        logger.info(f"emotion guide index: {self.emotion_guide_list.index(emotion_guide)}")
        agent_prompt = self.init_agent_prompt(chat_history, current_question, emotion_guide)
        _model_configs = self.init_agent_model_config(model_configs)

        router_agent_response = self.get_router_agent_response(current_question, router_agent_prompt, _model_configs["router_agent"])
        logger.info(f"router_agent_response: {router_agent_response}")

        for agent_key in ["agent_1", "agent_2", "agent_3", "agent_4"]:
            if agent_key in router_agent_response:
                agent_model_config = _model_configs[agent_key]
                if agent_model_config.model.startswith("gemini"):
                    prompt = GeminiPrompt(prompt=current_question, system_instruction=agent_prompt[agent_key])
                    # For Gemini API, create an async wrapper around the synchronous generator
                    gemini_generator = generate_text_with_stream(prompt, agent_model_config)
                    for chunk in gemini_generator:
                        yield chunk
                else:
                    # For local models, use our async generator
                    # For local models, use our sync generator
                    for chunk in local_model_generate_text_stream(
                        prompt=current_question,
                        system_instruction=agent_prompt[agent_key],
                        model_configs=agent_model_config
                    ):
                        yield chunk
                return  # Exit after finding the correct agent
        
        # If no agent found
        logger.info("No suitable agent found")
        yield ""