import copy
import json
import math
import os
from enum import Enum

from exception.generic_exception import GenericException
from infrastructure.log import Log

import jsons
import requests
from langchain.callbacks import get_openai_callback
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, BaseMessage, AIMessage


#   from langchain.globals import set_debug
# set_debug(True)


class ChatMessageType(Enum):
    SYSTEM = "SYSTEM"
    HUMAN = "HUMAN"
    ASSISTANT = "ASSISTANT"


class ChatMessage():
    type: ChatMessageType
    message: str

    def __init__(self, type: ChatMessageType, message: str) -> None:
        self.type = type
        self.message = message

    def __str__(self):
        return jsons.dumps(self, {"indent": 4})

    __repr__ = __str__


class ChatSystemMessage(ChatMessage):
    def __init__(self, message: str) -> None:
        super().__init__(ChatMessageType.SYSTEM, message)


class ChatHumanMessage(ChatMessage):
    def __init__(self, message: str) -> None:
        super().__init__(ChatMessageType.HUMAN, message)


class ChatAssistantMessage(ChatMessage):
    def __init__(self, message: str) -> None:
        super().__init__(ChatMessageType.ASSISTANT, message)


class ChatClientParams():
    chat_deployment: str
    openai_api_key: str
    temperature: float
    frequency_penalty: float
    presence_penalty: float
    top_p: float

    def __init__(self,
                 chat_deployment: str | None = None,
                 openai_api_key: str | None = None,
                 temperature: float | None = None,
                 frequency_penalty: float | None = None,
                 presence_penalty: float | None = None,
                 top_p: float | None = None) -> None:
        self.chat_deployment = chat_deployment if chat_deployment is not None else os.environ["OPENAI_CHAT_DEPLOYMENT"]
        self.openai_api_key = openai_api_key if openai_api_key is not None else os.environ["OPENAI_API_KEY"]
        self.temperature = temperature if temperature is not None else float(os.environ["OPENAI_TEMPERATURE"])
        self.frequency_penalty = frequency_penalty if frequency_penalty is not None else float(os.environ["OPENAI_FREQUENCY_PENALTY"])
        self.presence_penalty = presence_penalty if presence_penalty is not None else float(os.environ["OPENAI_PRESENCE_PENALTY"])
        self.top_p = top_p if top_p is not None else float(os.environ["OPENAI_TOP_P"])

    def __str__(self):
        new_self = self
        if hasattr(new_self, "openai_api_key"):
            new_self = copy.deepcopy(self)
            new_self.openai_api_key = "XXXXXXX"

        return jsons.dumps(new_self, {"indent": 4})

    __repr__ = __str__


class ChatClient():
    __instance = None
    __tokens_used: int = 0
    __input_tokens_used: int = 0
    __output_tokens_used: int = 0

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def ask(self, messages: list[ChatMessage], params: ChatClientParams) -> str:
        if os.environ["OPENAI_CALL_WITH_LIBRARY"] == "LANGCHAIN":
            return self.ask_with_langchain(messages, params)
        elif os.environ["OPENAI_CALL_WITH_LIBRARY"] == "REQUESTS":
            return self.ask_with_requests(messages, params)
        else:
            raise GenericException("OPENAI_CALL_WITH_LIBRARY environment variable not valid or not set. "
                                   f"Value: {os.environ['OPENAI_CALL_WITH_LIBRARY']}")

    def ask_with_requests(self, messages: list[ChatMessage], params: ChatClientParams) -> str:
        Log.debug("\n#############\nChatGPT Model Params With Requests:")
        Log.debug(str(params).replace(params.openai_api_key, "xxxxx"))
        Log.debug("##########\n")

        chat_messages: list[any] = []

        Log.debug("\n#############\nChatGPT Prompt With Requests:")

        for message in messages:
            match message.type:
                case ChatMessageType.SYSTEM:
                    chat_messages.append(
                        {
                            "role": "system",
                            "content": message.message
                        },
                    )
                case ChatMessageType.HUMAN:
                    chat_messages.append(
                        {
                            "role": "user",
                            "content": message.message
                        },
                    )
                case ChatMessageType.ASSISTANT:
                    chat_messages.append(
                        {
                            "role": "assistant",
                            "content": message.message
                        },
                    )
            Log.debug(f"\n{message.type}:\n{message.message}")

        Log.debug("############\n")

        openai_url_base = os.environ["OPENAI_API_BASE"]
        openai_version = os.environ["OPENAI_API_VERSION"]
        url = f"{openai_url_base}/{openai_version}/chat/completions"

        payload = {
            "messages": chat_messages,
            "model": params.chat_deployment,
            "stream": False,
            "n": 1,
            "temperature": params.temperature,
            "frequency_penalty": params.frequency_penalty,
            "presence_penalty": params.presence_penalty,
            "top_p": params.top_p
        }

        headers = {
            'Authorization': f"Bearer {params.openai_api_key}",
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise GenericException(f"ChatGPT Request failed. Status code: {response.status_code}. "
                                   f"Response: {response.text}")

        chat_response = json.loads(response.content)

        result = chat_response["choices"][0]["message"]["content"]

        total_tokens = chat_response["usage"]["total_tokens"]

        self.__tokens_used += total_tokens
        self.__input_tokens_used += chat_response["usage"]["prompt_tokens"]
        self.__output_tokens_used += chat_response["usage"]["completion_tokens"]

        Log.debug("\n#############\nChatGPT Response:")
        Log.debug(result)
        Log.debug("#############")
        Log.debug(f"Total tokens: {total_tokens}")
        Log.debug("#############\n")

        return result

    def ask_with_langchain(self, messages: list[ChatMessage], params: ChatClientParams) -> str:
        openai_chat = AzureChatOpenAI(
            azure_deployment=params.chat_deployment,
            max_retries=1,
            n=1,
            temperature=params.temperature,
            model_kwargs={
                "frequency_penalty": params.frequency_penalty,
                "presence_penalty": params.presence_penalty,
                "top_p": params.top_p,
            }
        )

        Log.debug("\n#############\nChatGPT Model Params With Langchain:")
        Log.debug(str(openai_chat).replace(os.environ["OPENAI_API_KEY"], "xxxxx"))
        Log.debug("##########\n")

        chat_messages: list[BaseMessage] = []

        Log.debug("\n#############\nChatGPT Prompt:")

        for message in messages:
            match message.type:
                case ChatMessageType.SYSTEM:
                    chat_messages.append(SystemMessage(content=message.message))
                case ChatMessageType.HUMAN:
                    chat_messages.append(HumanMessage(content=message.message))
                case ChatMessageType.ASSISTANT:
                    chat_messages.append(AIMessage(content=message.message))
            Log.debug(f"\n{message.type}:\n{message.message}")

        Log.debug("############\n")

        result = None
        with get_openai_callback() as cb:
            result = openai_chat(chat_messages)
            self.__tokens_used += cb.total_tokens
            self.__input_tokens_used += cb.prompt_tokens
            self.__output_tokens_used += cb.completion_tokens

            Log.debug("\n#############\nChatGPT Response:")
            Log.debug(result)
            Log.debug("#############")
            Log.debug(f"Total tokens: {cb.total_tokens}")
            Log.debug("#############\n")

        return result.content

    def tokens_used(self) -> int:
        return self.__tokens_used

    def input_tokens_used(self) -> int:
        return self.__input_tokens_used

    def output_tokens_used(self) -> int:
        return self.__output_tokens_used

    def total_cost(self) -> int:
        return (math.ceil(self.__input_tokens_used / 1000.0) * float(os.environ["OPENAI_INPUT_COST"])) + \
               (math.ceil(self.__output_tokens_used / 1000.0) * float(os.environ["OPENAI_OUTPUT_COST"]))

    def reset_usage(self):
        self.__tokens_used = 0
        self.__input_tokens_used = 0
        self.__output_tokens_used = 0
