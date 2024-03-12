import copy
import json
import os
from typing import Iterator

from llama_cpp.llama_grammar import LlamaGrammar
from tqdm import tqdm

from llm_orchestrator.llm_interface import LLMInterface


def main():
    model_path = os.path.join(".", "data", "models", "mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf")
    system_prompt_path = os.path.join(".", "data", "system_prompts", "system_prompt_planner.txt")
    questions_folder = os.path.join(".", "data", "test_set", "prompts")
    schema_path = os.path.join(".", "data", "json_schemas", "task_schema.json")

    node_to_id = {
        "Node1": {
            "Lightpath": set([2269, 2270, 2273, 2275, 2283, 2286, 2291, 2295]),
            "Service-1Gb": set([2272, 2274, 2279, 2280, 2282, 2284, 2287, 2288, 2289, 2290, 2292, 2294]),
            "Service-10Gb": set([2271, 2276, 2277, 2278, 2281, 2285, 2293, 2296]),
        },
        "Node2": {
            "Lightpath": set([2297, 2298, 2301, 2303, 2311, 2314, 2319, 2323]),
            "Service-1Gb": set([2300, 2302, 2307, 2308, 2310, 2312, 2315, 2316, 2317, 2318, 2320, 2322]),
            "Service-10Gb": set([2299, 2304, 2305, 2306, 2309, 2313, 2321, 2324]),
        },
        "Node3": {
            "Lightpath": set([2357, 2358, 2361, 2363, 2371, 2374, 2379, 2383]),
            "Service-1Gb": set([2360, 2362, 2367, 2368, 2370, 2372, 2375, 2376, 2377, 2378, 2380, 2382]),
            "Service-10Gb": set([2359, 2364, 2365, 2366, 2369, 2373, 2381, 2384]),
        },
    }

    # Load LLM to memory
    interface = LLMInterface(model_path, n_ctx=8192)

    # Create grammar
    schema = open(schema_path).read()
    grammar = LlamaGrammar.from_json_schema(schema)

    # Read system prompt
    system_prompt = open(system_prompt_path).read()

    # Loop over all the questions in the questions folder
    for question_file in tqdm(os.listdir(questions_folder)):
        question_path = os.path.join(questions_folder, question_file)
        question_id = question_file.split("_")[1].split(".")[0]

        # Check if prediction already exists. If yes, skip
        if os.path.exists(
            os.path.join(".", "data", "test_set", "predictions", "task_lists", f"prediction_{question_id}.json")
        ):
            continue
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

        try:
            task_parsed = json.loads(task_list)
        except json.JSONDecodeError as e:
            print(f"Error parsing the task list for question {question_id}")
            print(task_list)
            raise e

        available_ids = copy.deepcopy(node_to_id)
        # Assignment of nodes to source and sink interface IDs
        for task in task_parsed:
            if task["task"] != "Measurement":
                source_id = available_ids[task["source"]][task["task"]].pop()
                sink_id = available_ids[task["sink"]][task["task"]].pop()
                task["description"] += f" ID of the source interface: {source_id}, ID of the sink interface: {sink_id}"

        # Save the answer
        prediction_path = os.path.join(
            ".", "data", "test_set", "predictions", "task_lists", f"prediction_{question_id}.json"
        )
        with open(prediction_path, "w") as f:
            json.dump(task_parsed, f, indent=2)


if __name__ == "__main__":
    main()
