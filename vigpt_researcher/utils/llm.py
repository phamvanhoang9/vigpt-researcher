from __future__ import annotations

import logging
import json 
from fastapi import WebSocket 
from langchain_community.adapters import openai as lc_openai
from colorama import Fore, Style 
from typing import Optional, Any, Dict

from vigpt_researcher.master.prompts import auto_agent_instructions


def get_llm(llm_provider, **kwargs):
    match llm_provider:
        case "openai":
            from ..llm_provider import OpenAIProvider
            llm_provider = OpenAIProvider
        case "google":
            from ..llm_provider import GoogleProvider
            llm_provider = GoogleProvider
        case _:
            from vigpt_researcher.llm_provider import GenericLLMProvider
            return GenericLLMProvider.from_provider(llm_provider, **kwargs)
        
    return llm_provider(**kwargs)

async def create_chat_completion(
        messages: list,  # type: ignore
        model: Optional[str] = None,
        temperature: float = 0.9,
        max_tokens: Optional[int] = None,
        llm_provider: Optional[str] = None,
        stream: Optional[bool] = False,
        websocket: WebSocket | None = None,
        llm_kwargs: Dict[str, Any] | None = None
) -> str:
    """Create a chat completion using the OpenAI API
    Args:
        messages (list[dict[str, str]]): The messages to send to the chat completion
        model (str, optional): The model to use. Defaults to None.
        temperature (float, optional): The temperature to use. Defaults to 0.9.
        max_tokens (int, optional): The max tokens to use. Defaults to None.
        stream (bool, optional): Whether to stream the response. Defaults to False.
        llm_provider (str, optional): The LLM Provider to use.
        webocket (WebSocket): The websocket used in the currect request
    Returns:
        str: The response from the chat completion
    """

    # validate input
    if model is None:
        raise ValueError("Model cannot be None")
    if max_tokens is not None and max_tokens > 8001:
        raise ValueError(f"Max tokens cannot be more than 8001, but got {max_tokens}")
    
    # Ensure llm_kwargs is a dictionary
    if llm_kwargs is None:
        llm_kwargs = {}
    
    provider = get_llm(llm_provider, model=model, temperature=temperature, max_tokens=max_tokens, **llm_kwargs)
    
    response = ""

    # create response
    for attempt in range(10):  # maximum of 10 attempts
        response = await provider.get_chat_response(
            messages=messages, stream=stream, websocket=websocket
        )
        # response = await send_chat_completion_request(
        #     messages, model, temperature, max_tokens, stream, llm_provider, websocket
        # )
        
        return response

    logging.error("Failed to get response from {llm_provider} API after 10 attempts")
    raise RuntimeError("Failed to get response from {llm_provider} API after 10 attempts")


import logging


async def send_chat_completion_request(
        messages, model, temperature, max_tokens, stream, llm_provider, websocket
):
    if not stream:
        result = lc_openai.ChatCompletion.create(
            model=model,  # Change model here to use different models
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            provider=llm_provider,  # Change provider here to use a different API
        )
        """ 
        Documentation for OpenAI Chat Completion API:
        https://platform.openai.com/docs/guides/text-generation/chat-completions-api
        """
        return result["choices"][0]["message"]["content"] 
    else:
        return await stream_response(model, messages, temperature, max_tokens, llm_provider, websocket)


async def stream_response(model, messages, temperature, max_tokens, llm_provider, websocket=None):
    paragraph = ""
    response = ""

    for chunk in lc_openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            provider=llm_provider,
            stream=True,
    ):
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
            response += content
            paragraph += content
            if "\n" in paragraph:
                if websocket is not None:
                    await websocket.send_json({"type": "report", "output": paragraph})
                else:
                    print(f"{Fore.GREEN}{paragraph}{Style.RESET_ALL}")
                paragraph = ""
    return response


def choose_agent(smart_llm_model: str, llm_provider: str, task: str) -> dict:
    """Determines what server should be used
    Args:
        task (str): The research question the user asked
        smart_llm_model (str): the llm model to be used
        llm_provider (str): the llm provider used
    Returns:
        server - The server that will be used
        agent_role_prompt (str): The prompt for the server
    """
    try:
        response = create_chat_completion(
            model=smart_llm_model,
            messages=[
                {"role": "system", "content": f"{auto_agent_instructions()}"},
                {"role": "user", "content": f"task: {task}"}],
            temperature=0,
            llm_provider=llm_provider
        )
        agent_dict = json.loads(response)
        print(f"Agent: {agent_dict.get('server')}")
        return agent_dict
    except Exception as e:
        print(f"{Fore.RED}Error in choose_agent: {e}{Style.RESET_ALL}")
        return {"server": "Default Agent",
                "agent_role_prompt": "Bạn là một trợ lý nghiên cứu suy luận AI. Mục đích duy nhất của bạn là viết các báo cáo có cấu trúc tốt, được đánh giá cao về mặt phê bình, khách quan và có cấu trúc vững chắc về văn bản được giao."}