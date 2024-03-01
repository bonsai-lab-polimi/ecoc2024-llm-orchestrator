import os
from typing import Iterator

from llm_orchestrator.llm_interface import LLMInterface


def main():
    model_path = os.path.join(".", "llama.cpp", "models", "mistral-instruct-7b", "mistral-7b-instruct-v0.2.Q5_K_M.gguf")
    interface = LLMInterface(model_path)
    prompt = "[INST] Generate an example .json file. The JSON file must be wrapped in ```json [JSON file here] ```[/INST]"
    output = interface.generate(prompt)
    if not isinstance(output, Iterator):
        print(output["choices"][0]["text"])
    else:
        print(next(output)["choices"][0]["text"])


if __name__ == "__main__":
    main()
