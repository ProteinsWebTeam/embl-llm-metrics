# EMBLLMetrics

## Intro
The goal of EMBLLMetrics is to benchmark open and commercial LLMs across a variety of EBI-relevant tasks.
This will result in a leaderboard similar to [Open-LLM-Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard#/).
To achieve this, EMBLLMetrics uses the [Language Model Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) framework.


## Contents

#### Tasks
Folder containing `.yml` and `.py` configuration files (read more about this [New Task Guide](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/new_task_guide.md), [Task Guide](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/task_guide.md)). As mentioned in the guides, the tasks need to reference a dataset (HF or local one). The HF datasets we're currently using for testing are [bioc_llm](https://huggingface.co/datasets/apolignano/bioc_llm) and [biored_subset](https://huggingface.co/datasets/apolignano/biored_subset). These can be used as a reference on how to create a new one.


The `tasks` folder needs to be referenced with the `--include-path` param every time the `lm_eval` command is executed. It's the folder where the framework will look into for valid tasks. More on this below.

#### Scripts

- ##### compare_resps.sh - Compare ground truth (targe) with unfiltered and filtered answers from the LLM (last benchmark).

  Command structure
  
  ```./compare_resps.sh <results_path> <modelcompany__modelname>```

  Example
  
  ```./compare_resps.sh ../results google__gemma-2-2b-it```

  ![image](https://github.com/user-attachments/assets/57e52f7d-bb1f-4f15-8875-95321c08e111)


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


## Usage

#### Command structure
```
lm_eval
    --model <type_of_model:(hf|openai-completions)> \
    --model_args (pretrained=<hf_model_name>,parallelize=True | model=<api_model>) \
    --include_path <tasks_folder_path> \
    --tasks <task_name> \
    --output_path <path_where_to_store_results> \
    --batch_size 16 \
    --log_samples 
```

#### HuggingFace model example
```
lm_eval
    --model hf \
    --model_args pretrained=google/gemma-2-2b-it,parallelize=True \ 
    --include_path /hps/software/users/agb/interpro/apolignano/projects/embl_llm_metrics/tasks_test \
    --tasks bioc_llm_hf --batch_size 16 \
    --output_path=/hps/software/users/agb/interpro/apolignano/embl_llm_metrics/results \ 
    --log_samples
```

#### OpenAI model example
```
lm_eval
    --model openai-completions \
    --model_args model=o1-mini \
    --tasks bioc_llm_api \ 
    --output_path=/hps/software/users/agb/interpro/apolignano/embl_llm_metrics/results \ 
    --log_samples
```
