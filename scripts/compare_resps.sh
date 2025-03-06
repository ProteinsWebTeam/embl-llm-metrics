#!/bin/bash

# Accept the path and model name as CLI parameters
BASE_PATH=$1
MODEL_NAME=$2

# If either parameter is not provided, print usage and exit
if [ -z "$BASE_PATH" ] || [ -z "$MODEL_NAME" ]; then
  echo "Usage: $0 <base_path> <model_name>"
  exit 1
fi

# Run jq command with the path and model name as parameters
jq '{target: .target, resps: .resps, filtered_resps: .filtered_resps}' $(ls -t "$BASE_PATH/$MODEL_NAME"/*.jsonl | head -1)

