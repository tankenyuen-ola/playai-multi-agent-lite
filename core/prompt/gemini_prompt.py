from pydantic import BaseModel
from google.genai.types import Content, Part
import json

class GeminiPrompt(BaseModel):
    prompt: str
    system_instruction: str


class ChatHistory(BaseModel):
    chat_history: list[Content]
    
    def to_simple_format(self):
        """
        Convert the chat history to a simple format with role and content keys.
        
        Returns:
            str: A JSON string representation of the chat history.
        """
        simple_format = []
        for content in self.chat_history:
            # Extract the text from the first part
            text = content.parts[0].text if content.parts else ""
            simple_format.append({
                "role": content.role,
                "content": text
            })
        # Convert the list to a JSON string
        return json.dumps(simple_format, ensure_ascii=False)
    
    @classmethod
    def from_simple_format(cls, simple_format):
        """
        Create a ChatHistory object from a simple format with role and content keys.
        
        Args:
            simple_format (str): A JSON string representation of the chat history.
            
        Returns:
            ChatHistory: A ChatHistory object with the converted chat history.
        """
        # Parse the JSON string back to a list
        if isinstance(simple_format, str):
            simple_format = json.loads(simple_format, encoding='utf-8')
            
        chat_history = []
        for message in simple_format:
            chat_history.append(
                Content(
                    role=message["role"],
                    parts=[Part.from_text(text=message["content"])]
                )
            )
        return cls(chat_history=chat_history)
