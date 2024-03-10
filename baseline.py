import os
from typing import Iterator

from llm_orchestrator.llm_interface import LLMInterface


def main():
    model_path = os.path.join(".", "data", "models", "mistral-7b-instruct-v0.2.Q5_K_M.gguf")
    system_prompt_path = os.path.join(".", "data", "test_set", "system_prompt_baseline.txt")
    questions_folder = os.path.join(".", "data", "test_set", "prompts")
    prediction_folder = os.path.join(".", "data", "test_set", "predictions_baseline")
    schema_folder = os.path.join(".", "data", "json_schemas")

    # Load LLM to memory
    interface = LLMInterface(model_path, n_ctx=8192)
    task_to_schema_path = {
        "Lightpath": "lightpath_schema.json",
        "Measurement": "measurement_schema.json",
        "Service": "service_schema.json",
    }
    task_to_schema = {task: open(os.path.join(schema_folder, schema)).read() for task, schema in task_to_schema_path.items()}

    # Read system prompt
    system_prompt = open(system_prompt_path).read()

    for question_file in os.listdir(questions_folder):
        question_path = os.path.join(questions_folder, question_file)
        question_id = question_file.split("_")[1].split(".")[0]
        # Read the question
        question = "User: " + open(question_path).read()
        # Concatenate all the json schemas in one big string:
        context = ""
        for task, schema in task_to_schema.items():
            context = context + f"Schema for {task}:" + schema + "\n"
        # Generate the tokens for the full prompt
        # Mistral Instruct requires two special tokens to start and end the prompt
        tokens = interface.tokenize("[INST]" + system_prompt + question + "Assistant:\n" "[/INST]")
        output = interface.generate(tokens, max_tokens=0, seed=42)
        if not isinstance(output, Iterator):
            answer = output["choices"][0]["text"]
        else:
            answer = next(output)["choices"][0]["text"]
        # Save the answer
        prediction_path = os.path.join(prediction_folder, f"prediction_{question_id}.txt")
        with open(prediction_path, "w") as f:
            f.write(answer)


if __name__ == "__main__":
    main()
