# EMBLLMetrics

## Intro
The goal of EMBLLMetrics is to benchmark open and commercial LLMs across a variety of EBI-relevant tasks.
This will result in a leaderboard similar to [Open-LLM-Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard#/).
To achieve this, EMBLLMetrics uses the [Language Model Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) framework.


## Contents

#### Tasks
Folder containing `.yml` and `.py` configuration files (read more about this [New Task Guide](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/new_task_guide.md), [Task Guide](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/task_guide.md)).

This folder needs to be referenced every time the `lm_eval` command is executed with the `--include-path` param. It's the folder where the framework will look into for valid tasks. More on this below.

#### Scripts
- compare.sh
- process-results.sh
- publush-results.sh

## Pre-usage steps
- log in to the `slurm` cluster
- become `interpro`
- switch shell to `bash`
- Request a slurm job with GPUs `srun --time <time> --mem=64GB --gpus-per-node=<gpu_model>:<#_gpus> --pty bash`
- Run `setup_elm` to:
  - export necessary environment variables (i.e the virtualenv path and the HuggingFace home path)
  - activate the virtualenv


