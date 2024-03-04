from abc import ABC, abstractmethod
from typing import Any

from llama_cpp import Llama


class AbstractLLMInterface(ABC):
    @abstractmethod
    def generate(self, tokens: Any, **kwargs) -> Any:
        pass


class LLMInterface(AbstractLLMInterface):
    def __init__(self, model_path: str, **kwargs):
        self.llm = Llama(model_path=model_path, n_gpu_layers=-1, **kwargs)

    def generate(self, tokens: list[int], **kwargs):
        return self.llm.create_completion(tokens, **kwargs)

    def tokenize(self, prompt: str):
        return self.llm.tokenize(prompt.encode("utf-8"))
