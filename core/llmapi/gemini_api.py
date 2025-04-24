from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import logging
from core.prompt.gemini_prompt import GeminiPrompt
from core.config.model_config import GeminiModelConfig
from core.config.logging_config import setup_logger

# Set up logging
setup_logger()
logger = logging.getLogger(__name__)

load_dotenv()

def generate_text_with_stream(user_prompt: GeminiPrompt, model_config: GeminiModelConfig):

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY")
    )

    model = model_config.model
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_prompt.prompt),
            ],
        ),
    ]

    logger.info(f"system instruction: {user_prompt.system_instruction}")
    logger.info(f"Prepared user prompt: {user_prompt.prompt}")
    logger.info(f"Model: {model} , temperature: {model_config.temperature}, top_p: {model_config.top_p}, max_tokens: {model_config.max_tokens}")

    generate_content_config = types.GenerateContentConfig(
        temperature=model_config.temperature,
        top_p=model_config.top_p,
        max_output_tokens=model_config.max_tokens,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=user_prompt.system_instruction),
        ],
    )
    logger.debug(f"Generated content config with temperature: {model_config.temperature}, top_p: {model_config.top_p}")

    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            yield chunk.text
        logger.info("Text generation with streaming completed successfully")
    except Exception as e:
        logger.error(f"Error during text generation with streaming: {str(e)}")
        raise


def generate_text(user_prompt: GeminiPrompt, model_config: GeminiModelConfig):

    client = genai.Client(
        # api_key=os.environ.get("GEMINI_API_KEY"),
        api_key=os.environ.get("GEMINI_API_KEY"),
        #api_key='AIzaSy************7g',
        http_options=types.HttpOptions(api_version='v1beta')
    )

    model = model_config.model
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_prompt.prompt),
            ],
        ),
    ]

    logger.info(f"system instruction: {user_prompt.system_instruction}")
    logger.info(f"Prepared user prompt: {user_prompt.prompt}")
    logger.info(f"Model: {model} , temperature: {model_config.temperature}, top_p: {model_config.top_p}, max_tokens: {model_config.max_tokens}")


    generate_content_config = types.GenerateContentConfig(
        temperature=model_config.temperature,
        top_p=model_config.top_p,
        max_output_tokens=model_config.max_tokens,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=user_prompt.system_instruction),
        ],
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        logger.info("Text generation completed successfully")
        return response.text
    except Exception as e:
        logger.error(f"Error during text generation: {str(e)}")
        raise


if __name__ == "__main__":
    # Configure logging for the main script
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info("Starting Gemini API test")
    try:
        for chunk in generate_text_with_stream():
            print(chunk, end="")
        logger.info("Gemini API test completed successfully")
    except Exception as e:
        logger.error(f"Error during Gemini API test: {str(e)}")
