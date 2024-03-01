from abc import ABC, abstractmethod
from typing import Any

from llama_cpp import Llama


class AbstractLLMInterface(ABC):
    @abstractmethod
    def generate(self, prompt: Any) -> Any:
        pass


class LLMInterface(AbstractLLMInterface):
    def __init__(self, model_path: str, **kwargs):
        self.llm = Llama(model_path=model_path, n_gpu_layers=-1, **kwargs)

    def generate(self, prompt: str):
        return self.llm(prompt, max_tokens=0, echo=False)
