### Optical network orchestrator based on Large Language Models

To run this repository, clone a Mistral-Instruct LLM in .gguf format from [here](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF) and place it in data/

The repository is structured as follows:
- `data/` contains all data used for evaluation.
- llm_orchestrator/ contains Python scripts for querying the LLM-based orchestrator.
- sample_test.py runs a single illustrative query of the orchestrator.
- run_tests.py runs the experiments described in the paper.
