#!/bin/bash
set -e



python /app/code.py \
--input_path $1 \
--output_path $2 \
--series_instance_uid $3