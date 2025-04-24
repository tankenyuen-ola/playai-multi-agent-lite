from fastapi import APIRouter, HTTPException, Response, Body, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from fastapi.responses import StreamingResponse
from core.orchestra import AgentOrchestra
from core.config.model_predefine_config import predefine_gemini_configs, predefine_qwen_configs
import openai
import uuid
import time
import json
import os
from transformers import AutoTokenizer
import asyncio
import logging
import traceback


# Create router instance
router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "Not found"}},
)

# Create router instance
openai_router = APIRouter(
    prefix="/v1",  # Using /v1 prefix like OpenAI
    tags=["openai-compatible"],
    responses={404: {"description": "Not found"}},
)

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Pydantic models for request/response
class AgentRequest(BaseModel):
    """Model for agent creation request"""
    name: str
    role: str
    capabilities: Optional[List[str]] = None

class AgentResponse(BaseModel):
    """Model for agent response"""
    id: str
    name: str
    role: str
    capabilities: List[str]
    status: str

# New model for multi-agent request
class MultiAgentRequest(BaseModel):
    """Model for multi-agent request"""
    chat_history: str 
    # format [{"role": "user", "content": "user_message"},
    #        {"role": "AI character name", "content": "AI_message"}]

    current_question: str

class InputData(BaseModel):
    point: str
    #data: Dict[str, Any]

# @router.post("/api/dify/receive")
# async def dify_receive(
#     data: InputData = Body(...),
#     authorization: str = Header(None)
# ):
#     expected_api_key = "playai-dify"  # Replace with your actual API key
#     auth_scheme, _, api_key = authorization.partition(' ')

#     if auth_scheme.lower() != "bearer" or api_key != expected_api_key:
#         raise HTTPException(status_code=401, detail="Unauthorized")

#     # Process the incoming data
#     query = data.point
#     inputs = data.data

#     # Implement your logic here
#     content = {
#         "result": f"Received query: {query} with inputs: {inputs}"
#     }

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {expected_api_key}"
#     }

#     return JSONResponse(content=content, headers=headers)

### chat completions blocking mode
# @openai_router.post("/chat/completions")
# async def openai_chat_completions(request: Request, authorization: str = Header(None)):
#     """
#     OpenAI-compatible endpoint that processes requests and routes to your multi-agent system
#     """
#     #tokenizer = AutoTokenizer.from_pretrained("/data/llamafactory_model/Qwen2.5-7B-Instruct")
#     #prompt_tokens = completion_tokens = total_tokens = 0

#     # Validate authorization
#     expected_api_key = "playai-dify"  # Your API key
#     auth_scheme, _, api_key = authorization.partition(' ')

#     if auth_scheme.lower() != "bearer" or api_key != expected_api_key:
#         raise HTTPException(status_code=401, detail="Unauthorized")
    
#     # Parse the request body
#     try:
#         body = await request.json()
#         # model = body.get("model", "qwen")
#         messages = body.get("messages", [])
#         #stream = body.get("stream", False)
#         point = body.get("point", "qwen")
        
#         # Convert OpenAI messages format to your expected format
#         chat_history = json.dumps(messages[:-1]) if len(messages) > 1 else "[]"
#         current_question = messages[-1]["content"] if messages else ""
        
#         # Create a request object for your existing function
#         multi_agent_req = MultiAgentRequest(
#             chat_history=chat_history,
#             current_question=current_question
#         )
        
#         # Route to the appropriate handler based on the point
#         if point == "gemini":
#             # Call your existing function
#             result = await multi_agent_response_gemini(multi_agent_req)
#             response_content = result["response"]
#         elif point == "qwen":
#             # Call your qwen function
#             result = await multi_agent_response_qwen(multi_agent_req)
#             response_content = result["response"]

#             # # Count prompt tokens
#             # prompt_tokens = sum(len(tokenizer.encode(message["content"])) for message in messages)

#             # # Count completion tokens
#             # completion_tokens = len(tokenizer.encode(response_content))

#             # # Total tokens
#             # total_tokens = prompt_tokens + completion_tokens
#             # # response_content = "Qwen not implemented in this example"
        
#         # Return in OpenAI's expected format
#         return {
#             "id": f"chatcmpl-{uuid.uuid4()}",
#             "object": "chat.completion",
#             "created": int(time.time()),
#             "model": point,
#             "choices": [
#                 {
#                     "index": 0,
#                     "message": {
#                         "role": "assistant",
#                         "content": response_content
#                     },
#                     "finish_reason": "stop"
#                 }
#             ],
#             "usage": {
#                 "prompt_tokens": 0,  # You might want to implement actual token counting
#                 "completion_tokens": 0,
#                 "total_tokens": 0
#             }
#         }
    
#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"error": {"message": f"Error: {str(e)}", "type": "internal_error"}}
#         )


### chat completions streaming mode
@openai_router.post("/chat/completions")
async def openai_chat_completions(request: Request, authorization: str = Header(None)):
    #tokenizer = AutoTokenizer.from_pretrained("/data/llamafactory_model/Qwen2.5-7B-Instruct")
    #prompt_tokens = completion_tokens = total_tokens = 0

    # Validate authorization
    #expected_api_key = os.environ.get("OPENAI_DIFY_API_KEY") # Your API key
    expected_api_key = "playai-dify"  # Your API key
    auth_scheme, _, api_key = authorization.partition(' ')

    if auth_scheme.lower() != "bearer" or api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        body = await request.json()
        # model = body.get("model", "qwen")
        messages = body.get("messages", [])
        stream = True
        point = body.get("point", "gemini")
        # stream = body.get("stream", True)

        chat_history = json.dumps(messages[:-1]) if len(messages) > 1 else "[]"
        current_question = messages[-1]["content"] if messages else ""

        multi_agent_req = MultiAgentRequest(
            chat_history=chat_history,
            current_question=current_question
        )

        if stream:
            async def token_stream():
                try:
                    if point == "qwen":
                        orchestra = AgentOrchestra()
                        generator = orchestra.multi_agent_response_local_stream(
                            chat_history=multi_agent_req.chat_history,
                            current_question=multi_agent_req.current_question,
                            model_configs=predefine_qwen_configs
                        )
                        
                        # Iterate synchronously over the generator
                        for chunk in generator:
                            yield f"data: {json.dumps({'id': 'stream-test','object': 'chat.completion.chunk','created': int(time.time()),'model': point,'choices': [{'index': 0, 'delta': {'role': 'assistant', 'content': chunk},'finish_reason': None}]})}\n\n"
                            # await asyncio.sleep(0.1)
                    elif point == "gemini":
                        orchestra = AgentOrchestra()
        
                        # Call the multi_agent_response method
                        generator = orchestra.multi_agent_response_with_stream_gemini(
                            chat_history=multi_agent_req.chat_history,
                            current_question=multi_agent_req.current_question,
                            model_configs=predefine_gemini_configs
                        )
                        for chunk in generator:
                            logger.info(f"Received chunk: {chunk}")  # Add debug logging
                            yield f"data: {json.dumps({'id': 'stream-test','object': 'chat.completion.chunk','created': int(time.time()),'model': point,'choices': [{'index': 0, 'delta': {'role': 'assistant', 'content': chunk},'finish_reason': None}]})}\n\n"
                finally:
                    # Send final done message
                    yield f"data: {json.dumps({'id': 'stream-test','object': 'chat.completion.chunk','created': int(time.time()),'model': point,'choices': [{'index': 0, 'finish_reason': 'stop'}]})}\n\n"
                    #yield "data: [DONE]\n\n"

            return StreamingResponse(token_stream(), media_type="text/event-stream")
        else:
            if point == "gemini":
                result = await multi_agent_response_local(multi_agent_req)
                response_content = result["response"]
            elif point == "qwen":
                result = await multi_agent_response_local(multi_agent_req)
                response_content = result["response"]

                # prompt_tokens = sum(len(tokenizer.encode(message["content"])) for message in messages)
                # completion_tokens = len(tokenizer.encode(response_content))
                # total_tokens = prompt_tokens + completion_tokens

            return {
                "id": f"chatcmpl-{uuid.uuid4()}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": point,
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response_content
                        },
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }
            }

    except Exception as e:
        logger.error(f"Error in /chat/completions: {e}", exc_info=True)

        # Return a JSON response with error details
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "message": str(e),
                    "type": e.__class__.__name__,
                    "traceback": traceback.format_exc()
                }
            }
        )
        # return JSONResponse(
        #     status_code=500,
        #     content={"error": {"message": f"Error: {str(e)}", "type": "internal_error"}}
        # )

@router.post("/api/dify/receive")
async def dify_receive(data: InputData = Body(...), authorization: str = Header(None)):
    """
    Receive API query data from Dify.
    """
    expected_api_key = "playai-dify"  # TODO Your API key of this API
    auth_scheme, _, api_key = authorization.partition(' ')

    if auth_scheme.lower() != "bearer" or api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    point = data.point

    # for debug
    print(f"point: {point}")

    if point == "ping":
        return {
            "result": "pong",
        }

@router.post("/dify/request")
async def dify_request(data: InputData = Body(...), authorization: str = Header(None)):
    """
    Receive API query data from Dify.
    """
    expected_api_key = "playai-dify"  # TODO Your API key of this API
    auth_scheme, _, api_key = authorization.partition(' ')

    if auth_scheme.lower() != "bearer" or api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")

    point = data.point

    # for debug
    print(f"point: {point}")

    if point == "connect":
        return {
            "result": "Connect to Dify API successfully",
        }
    if point == "gemini":
        return multi_agent_response_gemini
    elif point == "qwen":
        return multi_agent_response_qwen

    raise HTTPException(status_code=400, detail="Not implemented")

@router.post("/multi-agent/gemini")
async def multi_agent_response_gemini(request: MultiAgentRequest):
    """
    Get a response from the multi-agent system
    """
    try:
        # Create an instance of AgentOrchestra
        orchestra = AgentOrchestra()
        
        # Call the multi_agent_response method
        response = orchestra.multi_agent_response_local(
            chat_history=request.chat_history,
            current_question=request.current_question,
            model_configs=predefine_gemini_configs
        )
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
    
@router.post("/multi-agent/qwen")
async def multi_agent_response_qwen(request: MultiAgentRequest):
    """
    Get a response from the multi-agent system with local models config
    """
    try:
        # Create an instance of AgentOrchestra
        orchestra = AgentOrchestra()
        
        # Call the multi_agent_response method
        response = orchestra.multi_agent_response_local(
            chat_history=request.chat_history,
            current_question=request.current_question,
            model_configs=predefine_qwen_configs
        )
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@router.post("/multi-agent/stream")
async def multi_agent_response_qwen_stream(request: MultiAgentRequest):
    """
    Get a streaming response from the multi-agent system
    """
    try:
        # Create an instance of AgentOrchestra
        orchestra = AgentOrchestra()

        # Obtain the synchronous generator
        generator = orchestra.multi_agent_response_local_stream(
            chat_history=request.chat_history,
            current_question=request.current_question,
            model_configs=predefine_qwen_configs
        )

        # Return a StreamingResponse with the synchronous generator
        return StreamingResponse(generator, media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")