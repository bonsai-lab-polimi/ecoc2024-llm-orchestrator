import json
import os
from typing import Iterator

from llama_cpp.llama_grammar import LlamaGrammar

from llm_orchestrator.llm_interface import LLMInterface


def main():
    model_path = os.path.join(".", "data", "models", "mistral-7b-instruct-v0.2.Q5_K_M.gguf")
    system_prompt_path = os.path.join(".", "data", "test_set", "system_prompt_executor.txt")
    task_list_folder = os.path.join(".", "data", "test_set", "predictions", "task_lists")
    prediction_folder = os.path.join(".", "data", "test_set", "predictions", "json_data")
    schema_folder = os.path.join(".", "data", "json_schemas")

    # Load LLM to memory
    interface = LLMInterface(model_path, n_ctx=4096)
    task_to_schema_path = {
        "Lightpath": "lightpath_schema.json",
        "Measurement": "measurement_schema.json",
        "Service": "service_schema.json",
    }
    task_to_schema = {
        task: open(os.path.join(schema_folder, schema)).read() for task, schema in task_to_schema_path.items()
    }
    # Create dictionary of grammars
    grammars_dict = {}
    for task, schema in task_to_schema_path.items():
        schema_path = os.path.join(schema_folder, schema)
        grammars_dict[task] = LlamaGrammar.from_json_schema(open(schema_path).read())

    # Read system prompt
    system_prompt = open(system_prompt_path).read()

    # Loop over all the task lists in the task list folder
    for task_list_file in os.listdir(task_list_folder):
        task_list_path = os.path.join(task_list_folder, task_list_file)
        task_id = task_list_file.split("_")[1].split(".")[0]
        task_list = json.load(open(task_list_path))
        json_list = []
        for task in task_list:
            schema_name = task["type"]
            grammar = grammars_dict[schema_name]
            # Generate the tokens for the full prompt
            # Mistral Instruct requires two special tokens to start and end the prompt
            tokens = interface.tokenize(
                "[INST]" + system_prompt + task["description"] + "\n" + task_to_schema[schema_name] + "[/INST]"
            )
            json_command = interface.generate(tokens, max_tokens=0, seed=42, grammar=grammar)
            if not isinstance(json_command, Iterator):
                json_command = json_command["choices"][0]["text"]
            else:
                json_command = next(json_command)["choices"][0]["text"]
            json_list.append(json.loads(json_command))
        # Save the answer
        prediction_path = os.path.join(prediction_folder, f"prediction_{task_id}.json")
        with open(prediction_path, "w") as f:
            json.dump(json_list, f, indent=2)


if __name__ == "__main__":
    main()
