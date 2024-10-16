# Optical network orchestrator based on Large Language Models

## Installation
Simply clone this repository and install it as a package using pip:
```sh
$ git clone git@github.com:nicoladicicco/llm-orchestrator.git
$ cd llm-orchestrator
$ pip install -e .
```

## Usage
The repository is structured as a data folder and self-contained scripts for running the different components of the pipeline independently. Said code will be encapsulated into the `LLMInterface` class in the future.
- `data/` contains the LLM files, the test set, and the model outputs.
- `llm_orchestrator/` contains Python scripts for querying the LLM interface and the output validator.
- `planning.py` runs the planning phase of the pipeline, and saves the generated tasks in the test set folder.
- `execution.py` runs the execution phase of the pipeline, and saves the generated data structures in the test set folder.
- `baseline.py` runs the baseline algorithm (just LLM inference without the planning and execution phases), and saves the generated data structures in the test set folder.

To run the code, clone a Mixtral-Instruct LLM in .gguf format from [here](https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF) and place it in `data/models/`. Feel free to experiment with other models.

## ECOC 2024 paper
You may download the paper associated with this dataset here: (TBD)
