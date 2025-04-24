import requests
import pytest
import json

# Base URL for our API
BASE_URL = 'http://127.0.0.1:8000/agents'
# BASE_URL = "http://0.0.0.0:18090/agents"

def test_multi_agent_basic_question():
    """
    Test Case 1: Basic question with empty chat history
    Tests the multi-agent endpoint with a simple question and no prior chat history
    """
    # Prepare the request data
    test_data = {
        "chat_history": "",
        "current_question": "What is the capital of France?"
    }

    # Send POST request to the endpoint
    response = requests.post(f"{BASE_URL}/multi-agent", json=test_data)

    print(response.json())
    # Assertions to verify the response
    assert response.status_code == 200, "Expected successful response"
    
    # Parse the response JSON
    response_data = response.json()
    
    # Verify response structure
    assert "response" in response_data, "Response should contain 'response' field"
    assert isinstance(response_data["response"], str), "Response should be a string"
    assert len(response_data["response"]) > 0, "Response should not be empty"

def test_multi_agent_with_chat_history():
    """
    Test Case 2: Question with existing chat history
    Tests the multi-agent endpoint with a follow-up question and previous chat history
    """
    # Prepare the request data with chat history
    test_data = {
        "chat_history": """
        [{"role": "user", "content": "好无聊啊, 你有什么好玩的话题吗?"},
        {"role": "米辣", "content": "聊点啥好呢…要不咱来聊聊为啥鱼只有7秒记忆？"},
        """,
        "current_question": "看来你是爱自然科学的"
    }

    # Send POST request to the endpoint
    response = requests.post(f"{BASE_URL}/multi-agent/qwen", json=test_data)

    # Assertions to verify the response
    assert response.status_code == 200, "Expected successful response"
    
    # Parse the response JSON
    response_data = response.json()
    print(response_data)
    # Verify response structure and content
    assert "response" in response_data, "Response should contain 'response' field"
    assert isinstance(response_data["response"], str), "Response should be a string"
    assert len(response_data["response"]) > 0, "Response should not be empty"

if __name__ == "__main__":
    """
    Manual test execution section
    This allows running the tests directly without pytest
    """
    # print("Running Test Case 1: Basic question")
    # try:
    #     test_multi_agent_basic_question()
    #     print("✅ Test Case 1 passed!")
    # except AssertionError as e:
    #     print(f"❌ Test Case 1 failed: {str(e)}")
    # except requests.exceptions.RequestException as e:
    #     print(f"❌ Test Case 1 failed - Connection error: {str(e)}")

    print("\nRunning Test Case 2: Question with chat history")
    try:
        test_multi_agent_with_chat_history()
        print("✅ Test Case 2 passed!")
    except AssertionError as e:
        print(f"❌ Test Case 2 failed: {str(e)}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Test Case 2 failed - Connection error: {str(e)}")
