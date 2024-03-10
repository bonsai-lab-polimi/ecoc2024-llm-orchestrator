import json
import os
from typing import Iterator

from llama_cpp.llama_grammar import LlamaGrammar

from llm_orchestrator.llm_interface import LLMInterface


def main():
    model_path = os.path.join(".", "data", "models", "mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf")
    system_prompt_path = os.path.join(".", "data", "system_prompts", "system_prompt_planner.txt")
    questions_folder = os.path.join(".", "data", "test_set", "prompts")
    schema_path = os.path.join(".", "data", "json_schemas", "task_schema.json")

    # Load LLM to memory
    interface = LLMInterface(model_path, n_ctx=4096)

    # Create grammar
    grammar = LlamaGrammar.from_json_schema(open(schema_path).read())

    # Read system prompt
    system_prompt = open(system_prompt_path).read()

    # Loop over all the questions in the questions folder
    for question_file in os.listdir(questions_folder):
        question_path = os.path.join(questions_folder, question_file)
        question_id = question_file.split("_")[1].split(".")[0]
        # Read the question
        question = "User: " + open(question_path).read()
        # Generate the tokens for the full prompt
        # Mistral Instruct requires two special tokens to start and end the prompt
        tokens = interface.tokenize("[INST]" + system_prompt + question + "Assistant:\n" "[/INST]")
        task_list = interface.generate(tokens=tokens)
        output = interface.generate(tokens, max_tokens=0, seed=42, grammar=grammar)
        if not isinstance(output, Iterator):
            task_list = output["choices"][0]["text"]
        else:
            task_list = next(output)["choices"][0]["text"]
        task_parsed = json.loads(task_list)
        # Save the answer
        prediction_path = os.path.join(
            ".", "data", "test_set", "predictions", "task_lists", f"prediction_{question_id}.json"
        )
        with open(prediction_path, "w") as f:
            json.dump(task_parsed, f, indent=2)


if __name__ == "__main__":
    main()
