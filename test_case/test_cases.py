from core.config.model_config import ModelName
from core.prompt.gemini_prompt import ChatHistory
from core.config.model_predefine_config import predefine_qwen_configs
from google.genai.types import Content, Part
from core.orchestra import AgentOrchestra


def init_chat_history():
    """
    初始化一个空的聊天历史对象
    
    Returns:
        ChatHistory: 一个空的聊天历史对象
    """
    return ChatHistory(chat_history=[])

def update_chat_history(chat_history, user_message, model_response):
    """
    更新聊天历史，添加用户消息和模型响应
    
    Args:
        chat_history: 当前的聊天历史对象
        user_message: 用户的消息
        model_response: 模型的响应
        
    Returns:
        更新后的聊天历史对象
    """
    # 添加用户消息
    chat_history.chat_history.append(
        Content(
            role="user",
            parts=[Part.from_text(text=user_message)]
        )
    )
    
    # 添加模型响应
    chat_history.chat_history.append(
        Content(
            role="model",
            parts=[Part.from_text(text=model_response)]
        )
    )
    
    return chat_history

def interactive_chat():
    """
    交互式聊天函数，允许用户持续与模型对话
    """
    agent_orchestra = AgentOrchestra()
    chat_history = init_chat_history()
    
    print("欢迎使用多智能体聊天系统！输入 'exit' 或 'quit' 结束对话。")
    print("--------------------------------")
    
    while True:
        # 获取用户输入
        user_input = input("用户: ")
        
        # 检查是否退出
        if user_input.lower() in ['exit', 'quit']:
            print("感谢使用，再见！")
            break
        
        # 获取模型响应
        model_response = agent_orchestra.multi_agent_response(
            chat_history.to_simple_format(), 
            user_input, 
            predefine_qwen_configs
        )
        
        # 打印模型响应
        print("米辣:", model_response)
        
        # 更新聊天历史
        chat_history = update_chat_history(chat_history, user_input, model_response)
        
        print("--------------------------------")
    
    # 保存聊天历史到文件
    save_chat_history(chat_history)

def save_chat_history(chat_history):
    """
    将聊天历史保存到文件
    
    Args:
        chat_history: 聊天历史对象
    """
    # 转换为简单格式
    simple_format = chat_history.to_simple_format()
    
    # 保存到文件
    with open("chat_history.json", "w", encoding="utf-8") as f:
        f.write(simple_format)
    
    print("聊天历史已保存到 chat_history.json 文件")

def load_chat_history(file_path="chat_history.json"):
    """
    从文件加载聊天历史
    
    Args:
        file_path: 聊天历史文件路径
        
    Returns:
        聊天历史对象，如果文件不存在则返回初始化的聊天历史
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            simple_format = f.read()
        
        return ChatHistory.from_simple_format(simple_format)
    except FileNotFoundError:
        print(f"未找到聊天历史文件 {file_path}，将使用初始聊天历史")
        return init_chat_history()

if __name__ == "__main__":
    # 运行交互式聊天
    interactive_chat()
    
    # 测试用例部分（已注释掉）
    """
    agent_orchestra = AgentOrchestra()
    chat_history = init_chat_history()
   
    test_cases_prompt = [
        "怎么个躺法"
    ]

    for prompt in test_cases_prompt:
        print("--------------------------------")
        print("用户问:", prompt)
        print(agent_orchestra.multi_agent_response(chat_history.to_simple_format(), prompt, predefine_model_configs))

    print("--------------------------------")
    """

