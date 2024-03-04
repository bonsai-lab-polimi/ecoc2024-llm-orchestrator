# Optical network orchestrator based on Large Language Models

## Installation
Simply clone this repository and install it as a package using pip:
```sh
$ git clone git@github.com:nicoladicicco/llm-orchestrator.git
$ cd llm-orchestrator
$ pip install -e .
```

## Usage
The repository is structured as follows:
- `data/` contains the LLM files, the evaluation test, and the model outputs.
- `llm_orchestrator/` contains Python scripts for querying the LLM interface and the output validator.
- `sample_test.py` runs a single illustrative query of the LLM interface.
- `run_tests.py` runs the experiments described in the paper.

To run the code, clone a Mistral-Instruct LLM in .gguf format from [here](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF) and place it in `data/models`. Feel free to experiment with other models.
