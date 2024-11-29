from openai import OpenAI
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core import Settings
from dotenv import load_dotenv
from typing import Optional, List, Mapping, Any
from pydantic import PrivateAttr
import os
from logger_setup import setup_logger
logger = setup_logger(__name__)

load_dotenv()

class DeepSeekLLM(CustomLLM):
    _context_window: int = 3900
    _num_output: int = 256
    _name: str = "deepseek-chat"
    _client: Any = PrivateAttr()
    _api_key: str = os.getenv("OPENAI_API_SECRET_KEY")
    _base_url: str = "https://api.deepseek.com"

    def __init__(self):
        super().__init__() 
        self._client = OpenAI(api_key=self._api_key, base_url=self._base_url)

    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""
        return LLMMetadata(
            context_window=self._context_window,
            num_output=self._num_output,
            model_name=self._name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, messages: Optional[List[Mapping[str, Any]]] = None, **kwargs: Any) -> CompletionResponse:
        """Make a request to the DeepSeek API and return the response."""
        try:
            if not messages:
                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ]
            
            logging.info(f"Prompt: {prompt}")
            response = self._client.chat.completions.create(
                model=self._name,
                messages=messages,
                response_format={"type": "json_object"},
                stream=False,
            )
            return CompletionResponse(text=response.choices[0].message.content)
        except Exception as e:
            return CompletionResponse(text=f"Error: {e}")
        
    @llm_completion_callback()
    def stream_complete(
        self, prompt: str, **kwargs: Any
    ) -> CompletionResponseGen:
        """Stream responses from the DeepSeek API."""
        try:
            response = self._client.chat.completions.create(
                model=self._name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                stream=True,
            )
            for chunk in response:
                delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                yield CompletionResponse(text=delta)
        except Exception as e:
            yield CompletionResponse(text=f"Error: {e}")
            
if __name__ == "__main__":
     Settings.llm = DeepSeekLLM()
     llm = Settings.llm
     query = "What is the meaning of life why are we here?"
     response = llm.complete(prompt=query)
     print(response.text)
