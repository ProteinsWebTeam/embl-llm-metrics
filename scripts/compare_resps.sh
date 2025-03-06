#!/bin/bash

MODEL_NAME=$1

# If either parameter is not provided, print usage and exit
if  [ -z "$MODEL_NAME" ]; then
  echo "Usage: $0  <model_name>"
  exit 1
fi

# Run jq command with the path and model name as parameters
jq '{target: .target, resps: .resps, filtered_resps: .filtered_resps}' $(ls -t "../results/$MODEL_NAME"/*.jsonl | head -1)

