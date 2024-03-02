import os
from typing import Iterator

from llm_orchestrator.llm_interface import LLMInterface


def main():
    model_path = os.path.join(".", "data", "models", "mistral-7b-instruct-v0.2.Q5_K_M.gguf")
    system_prompt_path = os.path.join(".", "data", "test_set", "system_prompt.txt")
    question_path = os.path.join(".", "data", "test_set", "prompts", "prompt_1.txt")
    answer_path = os.path.join(".", "data", "test_set", "ground_truths", "answer_1.json")

    interface = LLMInterface(model_path, n_ctx=8192, stream=True)
    prompt = "[INST] "
    context = ""

    # Read system prompt
    system_prompt = open(system_prompt_path).read()
    prompt += system_prompt
    # Read the question
    prompt += open(question_path).read()
    # Read the context
    schema_folder = os.path.join(".", "data", "json_schemas")
    for file in os.listdir(schema_folder):
        with open(os.path.join(schema_folder, file)) as f:
            context += f"Schema file for {file}:\n"
            context += f.read()
    prompt += context
    # Close prompt
    prompt += "[/INST]"

    output = interface.generate(prompt)
    if not isinstance(output, Iterator):
        print(output["choices"][0]["text"])
    else:
        print(next(output)["choices"][0]["text"])


if __name__ == "__main__":
    main()
